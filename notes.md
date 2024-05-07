# Notes

## About Gunicorn

- Gunicorn takes the place of the flask development server. It is intended for production use. I believe you can technically still use the embedded flask server, but Gunicorn might be more "best practice."

- To start the server, use the following syntax:

```sh
guincorn [name of the file that the app object is in]:[the name of the app object itself]
```

## Git integration

Your identification has been saved in /home/ubuntu/.ssh/id_ed25519
Your public key has been saved in /home/ubuntu/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:2AveGrVi9ZrUctGOyKpRcGLMJOpWnUL2hzVSqfHh02g chrishoina@gmail.com
The key's randomart image is:
+--[ED25519 256]--+
|  .o...+.        |
| .o=o.=o.        |
|.  o*=*.+        |
|. ...=.E . .     |
| o    = S . .    |
|.    o * * +     |
|    . = O = .    |
|     o * =       |
|    ..o o        |
+----[SHA256]-----+

# JWT libraries https://jwt.io/libraries?language=Python