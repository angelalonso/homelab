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
       

## Wishlist
- Authentication local machine -> yxc server
- Authentication yxc server -> regular server
