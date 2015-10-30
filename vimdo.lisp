(asdf:load-system :cl-termbox)
(asdf:load-system :cl-autowrap)

(defun draw-text (x y text &optional (fg-bg '(0 . 0))) 
  "execute a series of change-cell's in a sequential manner such as to write a line of text"
  (dotimes (i (length text))
    (termbox:change-cell (+ x i) y (char-code (nth i (coerce text 'list))) (car fg-bg) (cdr fg-bg))))

(defun test ()
    (termbox:init)
  (let ((items '("first item" "second item" "bored lets go throw knives at something")))
    (termbox:clear)
    (dotimes (i (length items))
      (draw-text 1 (1+ i) (nth i items)))
    ; ok i figured it out the fact that emacs is in a terminal instead of gui mode is disabling most of paredit's shortcuts
    (termbox:present)
    (autowrap:with-alloc (event '(:struct (termbox:tb-event)))
      (termbox:poll-event event)))
  (termbox:shutdown))

(test)
