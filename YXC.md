# YXC

Tool to manage a home cluster
Currently under development.

## Architecture

                              +------------------------------------+
                              |local machine                       |
                              |                                    |
                              |$yxc <object> <action> <parameters> |
                              |                                    |
                              +------------------------------------+
                                                |
                                                v
                                               API
                                                ^
                                                |
                                                |
                                           +----------+
                                           |yxc server|
                                           |          |
                                           |$yxc lead |
                                           |          |
                                           +----------+
                                                v
                        +------------+overwrite desired state+-----------+
                        |                   +        +                   |
                        |                   |        |                   |
           +------------v-+    +------------v-+    +-v------------+    +-v------------+
           |regular server|    |regular server|    |regular server|    |regular server|
           |              |    |              |    |              |    |              |
           |$yxc do       |    |$yxc do       |    |$yxc do       |    |$yxc do       |
           |              |    |              |    |              |    |              |
           +--------------+    +--------------+    +--------------+    +--------------+
       
## Progress
- [x] Read configs from yaml 
 - [x] servername
   - [x] ssh port
 - [x] user
   - [x] ssh keys (gitignore)
   - [x] group
- [x] Accept lead and do modes
- [x] API server
- [x] Modify config.yaml on API call
- [x] Communicate with regular server (get and set)

## Wishlist
- Authentication local machine -> yxc server
- Authentication yxc server -> regular server
