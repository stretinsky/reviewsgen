## Installation

1. Create a `.env` file from `.env.dist` and adapt it according to the needs of the application

    ```sh
    $ cp .env.dist .env && nano .env
    ```
    
2. Build and run the stack in detached mode

    ```sh
    $ docker-compose build
    $ docker-compose up -d
    ```
