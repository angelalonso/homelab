# ASD

Tool to manage a home cluster.

The name is an Acronym for All my Servers Do.  
  
Currently under development.  

## Architecture

                              +------------------------------------+
                              |local machine                       |
                              |                                    |
                              |$asd <object> <action> <parameters> |
                              |                                    |
                              +------------------------------------+
                                                |
                                                v
                                               API
                                                ^
                                                |
                                                |
                                           +----------+
                                           |asd server|
                                           |          |
                                           |$asd lead |
                                           |          |
                                           +----------+
                                                v
                        +------------+overwrite desired state+-----------+
                        |                   +        +                   |
                        |                   |        |                   |
           +------------v-+    +------------v-+    +-v------------+    +-v------------+
           |regular server|    |regular server|    |regular server|    |regular server|
           |              |    |              |    |              |    |              |
           |$asd do       |    |$asd do       |    |$asd do       |    |$asd do       |
           |              |    |              |    |              |    |              |
           +--------------+    +--------------+    +--------------+    +--------------+
       
## Progress
- [ok] Read configs from yaml 
- [x] Accept lead and do modes
- [x] API server
- [x] Modify config.yaml on API call
- [x] Communicate with regular server (get and set)

## Wishlist
- Authentication local machine -> asd server
- Authentication asd server -> regular server
