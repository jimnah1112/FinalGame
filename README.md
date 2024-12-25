# FinalGame
This is a survival game for our character Pingu. He has to eliminate the snowmans or he will be eliminated. Game was done in pygame using as reference videos by ClearCode in Pygame Tutorial
Link: https://www.youtube.com/watch?v=8OMghdHP-zs&t=21600s

```mermaid
graph TD
    A[Start] --> B[Penguin runs around the map]
    B --> C[Random Snowman appears]
    C --> D[Penguin attacks Snowman]
    D --> E{Is Snowman defeated?}
    E -->|Yes| F[Penguin continues running]
    E -->|No| D
    F --> G{Is there another Snowman?}
    G -->|Yes| C
    G -->|No| H[Penguin survives and wins]
