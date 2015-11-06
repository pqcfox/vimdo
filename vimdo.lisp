(asdf:load-system :cl-termbox)

(defun draw-text (x y text &optional (fg 0) (bg 0)) 
  "execute a series of change-cell's in a sequential manner such as to write a line of text"
  (dotimes (i (length text))
    (termbox:change-cell (+ x i) y (char-code (nth i (coerce text 'list))) fg bg)))

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
	 (if (eq selected i)
	     (draw-text 1 (1+ i) (nth i items) termbox:+white+ termbox:+black+)
	     (draw-text 1 (1+ i) (nth i items))))
       (termbox:present)
       (let ((event (termbox:poll-event)))
	 ; this is how we get the "ch" field of the "event" variable with type "tb-event"
	 ; its an int so we need to convert it to a char
	 (case (code-char (getf (termbox:event-data event) :ch))
	   (#\j
	    (setf selected (mod (1+ selected) (length items))))
	   (#\k
	    (setf selected (mod (1- selected) (length items))))
	   (#\q
	    (setf running nil)))
	 (termbox:free-event event))))
  (termbox:shutdown))

(test)
