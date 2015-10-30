(asdf:load-system :cl-termbox)
(asdf:load-system :cl-autowrap)

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
	     (draw-text 1 (1+ i) (nth i items) (termbox:tb-const "TB_WHITE") (termbox:tb-const "TB_BLACK"))
	     (draw-text 1 (1+ i) (nth i items))))
       (termbox:present)
       (autowrap:with-alloc (event '(:struct (termbox:tb-event)))
	 (termbox:poll-event event)
	 ; this is how we get the "ch" field of the "event" variable with type "tb-event"
	 ; its an int so we need to convert it to a char
	 (case (code-char (termbox:tb-event.ch event))
	   (#\j
	    (setf selected (mod (1+ selected) (length items))))
	   (#\k
	    (setf selected (mod (1- selected) (length items))))
	   (#\q
	    (setf running nil))))))
  (termbox:shutdown))

(test)
