#!/bin/bash

# In production:
# 1. Uncomment the code bellow with `Ctrl + ;`
# 2. `Shift + Alt + Arrow Down` and copy 20 times.
# 3. `Shift + Left Click` to place multiple cursors right before the `x`s
# 4. Change the first digit to: 1, 2, 3, ... 9.
# 5. Comment the debugging code.

# Production code:
# vitae ingest x0 x1 x2 x3 x4 --logs logs/x/0/ &
# vitae ingest x5 x6 x7 x8 x9 --logs logs/x/5/ &

# Debugging code:
vitae ingest 00 01 --log logs/00 &
vitae ingest 02 --logs logs/01 &
vitae ingest 11 99 --logs logs/02 &

# Wait for all background jobs to finish
wait
echo "All processes finished."