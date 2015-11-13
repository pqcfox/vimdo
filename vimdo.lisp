(asdf:load-system :cl-termbox)

(defun draw-text (x y text &optional (fg 0) (bg 0)) 
  "execute a series of change-cell's in a sequential manner such as to write a line of text"
  (dotimes (i (length text))
    (termbox:change-cell (+ x i) y (char-code (nth i (coerce text 'list))) fg bg)))

(defparameter *bindings* `(:ch (#\j :down
				#\k :up
				#\q :quit
				#\d :delete)
			   :key (,termbox:+key-esc+ :quit)))

(defun test ()
  (termbox:init)
  (let ((items '("first item" "second item" "bored lets go throw knives at something"))
	(selected 0)
	(running t))
    (loop
       (unless running
	 (return))
       (termbox:clear)
       (dotimes (i (length items))
	 (apply #'draw-text 1 (1+ i) (nth i items) (if (eq selected i)
						       (list termbox:+white+ termbox:+black+)
						       (list termbox:+default+ termbox:+default+))))
       (termbox:present)
       (let* ((event (termbox:poll-event))
	      (event-data (termbox:event-data event))
	      (ch (getf event-data :ch))
	      (key (getf event-data :key))
	      (bindings (getf *bindings* (if (not (= ch 0)) :ch :key))))
	 ; this is how we get the "ch" field of the "event" variable with type "tb-event"
	 ; its an int so we need to convert it to a char
	 (if (not (= ch 0))
	   (case (getf bindings (code-char ch))
	     (:down
	      (setf selected (mod (1+ selected) (length items))))
	     (:up
	      (setf selected (mod (1- selected) (length items))))
	     (:quit
	      (setf running nil))
	     (:delete
	       (if (plusp (length items))
		 (setf selected (max 0 (1- selected))
		       items (remove (nth selected items) items :test #'string=)))))
	   (case (getf bindings key)
	     (:quit
	      (setf running nil))))
	 (termbox:free-event event))))
  (termbox:shutdown))

(test)
