_This project has been part of the 42 curriculum by finorako, nyramana_

# PAC-MAN

<!--toc:start-->
- [PAC-MAN](#pac-man)
  - [Description](#description)
  - [Instructions](#instructions)
  - [Ressources](#ressources)
  - [Configuration](#configuration)
  - [Highscore](#highscore)
  - [Maze Generation](#maze-generation)
  - [Implementation](#implementation)
  - [General software Architecture](#general-software-architecture)
    - [GUI](#gui)
    - [MazeGenerator module](#mazegenerator-module)
    - [Entity](#entity)
    - [Rendering](#rendering)
  - [Project Management](#project-management)
<!--toc:end-->

## Description

Pac-man, this game was part of the long running community of game r since decades ago, it became a culte even. And here with this project, we tried to implement it with the pygame-ce library as the gui.

## Instructions

To play this `Pac-man` game you have the following choice bellow:

- Using the binary in the `itch.io` websit and just run it with the **config** (will be explained better in [this section](#configuration))
- You can also run it via the command line: just run: `uv run python -m pacman.py <config.json>` it will install automatically all the packages needed to lunch the program.

## Ressources

Peer to peer was the main ressources we used to complete this project. But stack overflow and slack was also part of it.

## Configuration

The configuration is should be in a json format that can handle python commentary (when the line starts with # it is considered as a commentary).

Bellow is an example:

```
{
 "pacgum_number": 1,
 "points_per_pacgum": 2,
 "points_per_super_pacgum": 5,
 # this is a commentary
 "points_per_ghost": 10,
 "level_max_time": 5,
 "life": 3,
 "seed": 42,
 "level_count": 10
}
```

## Highscore

For the high score, we decided to store it in a simple json file as it's easer to manipulate without the need of other dependencies to manipulate it.

Bellow is an example of how we store it:

```
[
    {
        "player_name": "this",
        "player_score": 1405,
        "player_time": 120
    },
    {
        "player_name": "sdfesfesd",
        "player_score": 104,
        "player_time": 90
    },
 ...
]
```

## Maze Generation

Provided with the subject of this project, there was a package that we must use a `MazeGenerator` it can generate a maze with 42 logo in it. And so we used it to generate a maze for us and using it's api we communicate with it to render that maze onto the screen.

## Implementation

- For the ghost we went with a simple yet effective way so that it doesn't include a lot of change or other implementation. A ghost has three behavior; the first one is:

- - `find direciton`: in this state it just randomly find direction each turn.
- - `chase player`: in this state as long as the player is in it's line of vision it will follow the player based on a simple bfs algorithm to find the shortest path.
- - `escape player`: in this state as long as it can be eaten it will randomly choose a direction that doesn't lead to the player.

The best part of the ghost implementation is that we made it so that every time the player complete a level we increase the line of sight of each ghost so that we don't need to tune the algorithm as it depends on the line of sight of the ghost.

## General software Architecture

### GUI

We where limited to only using functions that has an equivalence inside the mlx library, so that's why
by using the pygame-ce library we limited the use of the APIs to only the bare minimum.


For the GUI we used the following APIs and their equivalence in the mlx library.

| PYGAME | MLX |
| ------- | ---- |
| pygame.Surface | mlx.mlx_new_window |
| pygame.event | mlx.mlx_hook |
| pygame.Surface.set_at | mlx.mlx_put_pixel |
| pygame.display.set_mode | mlx.mlx_new_window |
| pygame.display.set_caption | a parameter of mlx.mlx_new_window|
| pygame.mouse.get_pos | mlx.mlx_mouse_hook |
| pygame.keys.get_just_pressed | mlx.mlx_key_hook |


### MazeGenerator module

How did we use the `MazeGenerator` module

| API | explanation |
| ---- | ----------- | | generate | This method generate a maze for us, it return a list of list integer that represent the wall for the current cell |
| _find_short_path | As we where allowed to use this module as we like without changing the content, we just used this method to generate the shortest path for the ghost for searching the player |


### Entity

The entity class, representing a player is used as the base class for all the players/ghost

| Class | Description |
| :--- | :--- |
| Entity | base class for players/ghost |
| Player | player representation |
| Ghost | Ghost representation |


### Rendering

The naming here is a bit confusing but in a sense, this is the class that combine all our functionalities
it contain all the necessary functions so that our project work perfectly.

| Rendering API | Description |
| :---- | :----: |
| run | Running the game simulation |
| update | updating what is on the screen |
| render | Render onto the screen what happen behind |
| get_event | getting event from the current screen, such as changing player direction for exampl |
| load_background | loading the background |

## Project Management

To make it so that our workflow work in the correct path and avoid conflict as possible, we assign each a role,
`nyramana` for the rendering part and `finorako` for the backend stuff and by doing it that way we avoided as
much as possible conflict and conducted a better workflow. It is also worth notice that when doing this project,
when revewing the PR we can make some descision on how to change or twinking the code to be merged with that
we made it so that the we understand each the codes of the others without much effort.

Here is a link to our project management other than the provided inside `PROJECT Management` directory: [project management](https://github.com/users/finorak/projects/2/views/1)
