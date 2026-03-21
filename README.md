# Django AI Music System

## Project Overview
This project is a Django-based system that models an AI music generation platform. 
The system focuses on the domain layer, including users, songs, and libraries, 
as well as database persistence and CRUD operations.


## Domain Model

### Core Domain Entities
- **User**: Represents a user who can create songs and manage libraries.
- **Song**: Represents a generated song.
- **Library**: Represents a collection of songs owned by a user.

### Relationships
- User (1) ——— generates ——> (0..*) Song
- User (1) ——— has ———> (1..*) Library
- Library (1) —— contains ——> (0..*) Song

### Enumerations
- **Mood**: happy, sad, romantic, relaxed, energetic, calm, angry
- **Genre**: pop, rock, jazz, classical, hiphop, r&b
- **SongVisibility**: private, public
- **Status**: pending, processing, completed


## Project Setup
### 1. Clone Repository
```
git clone https://github.com/Chanunchida-Dithakumarn/djangoAIMusic.git
cd djangoAIMusic
```

### 2. Install Dependencies
```
pip install django
```

### 3. Run Migrations
```
python manage.py migrate
```

### 4. Run Server
```
python manage.py runserver
```


## CRUD Functionality
### Create
- Add user
![Create User](images/add_user.png)
- Add song
![Create Song](images/add_song.png)
- Add library
![Create Library](images/add_library.png)

### Read
- View song list
![Song List](images/song_list.png)

### Update
- Edit song details
![Update song detail](images/change_song_detail.png)

### Delete
- Delete song
![Delete Song](images/after_delete_song.png)
