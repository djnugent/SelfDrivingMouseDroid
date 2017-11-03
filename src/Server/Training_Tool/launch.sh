#/bin/bash
SESSION_NAME="trainer"
tmux kill-session -t ${SESSION_NAME}
# create the session and first window
tmux new-session -d -s ${SESSION_NAME}
tmux send-keys -t ${SESSION_NAME} "htop"
# TensorBoard
tmux new-window -n tensorboard -t ${SESSION_NAME}
tmux send-keys -t ${SESSION_NAME}:1 "tensorboard --port 8081 --logdir /remote/rs/ecpeprime/training_logs"
# Flask
tmux new-window -n flask -t ${SESSION_NAME}
tmux send-keys -t ${SESSION_NAME}:2 "bash"
tmux send-keys -t ${SESSION_NAME}:2 "python flask_app.py"
tmux attach -t ${SESSION_NAME}
