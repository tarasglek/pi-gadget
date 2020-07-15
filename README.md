cvlc v4l2:///dev/video1:chroma=mjpg   --sout '#standard{access=http,mux=ts,mime=video/ts,dst=:5901}'
vlc http://localhost:5901
