Gaminator
-ver 0.3

Gaminator is an open-source library of Micropython games made to run on a Raspberry PI Pico with a Waveshare 1.3 inch, 240x240, LCD display (with small adjustements, can be used on any display).
Currently, it includes 5 games:
1. Barried Ball - Pong for one player
   ![IMG_20230823_172425](https://github.com/drclcomputers/Gaminator/assets/132164125/ead3e32a-d9bc-4709-a47c-4ef8fcffecab)

2. Flappy Pico - Try to avoid the pipes, while flying a red cube (imagine it's a bird)
   ![IMG_20230823_173059](https://github.com/drclcomputers/Gaminator/assets/132164125/228c0915-6ab6-4f6d-8261-873560029100)

3. Shooter Man - Control a man willing exterminate as many zombies as he can
   ![IMG_20230823_173154](https://github.com/drclcomputers/Gaminator/assets/132164125/c828d0d9-1d48-4d95-a6bc-713e0fd45b71)

4. Space Battle - Protect yourself as the asteroids fly towards you
   ![IMG_20230823_173314](https://github.com/drclcomputers/Gaminator/assets/132164125/6a5b1aba-4053-40a1-92d7-e92e32b9f87e)

5. Alien Outbreak - Avoid aliens' lasers and try to destroy them
   ![IMG_20230823_172254](https://github.com/drclcomputers/Gaminator/assets/132164125/f355b25f-8042-47f6-939b-bd409e4ef80a)

This library also includes a testing program to verify if all the controls are working.
![IMG_20230823_173346](https://github.com/drclcomputers/Gaminator/assets/132164125/d11eb5cb-44d2-44a6-be5c-10f6bd9fdb4d)

I created a simple interface to start any games on the pi pico, without the need to connect to a computer (Note: You'll need a computer to load all the games and other programs).
![IMG_20230823_173407](https://github.com/drclcomputers/Gaminator/assets/132164125/e2971a3c-6043-40c5-a2df-a66a24cd9303)


Future plans:
- Add splash screens when opening the games
- Enhence the visuals of the games (Now, they are very simple with simple geometric figures and basic colors)
- Add sounds and music via a Buzzer Speaker
- Add more games
- Add a battery to power the Gaminator on the go
- Create a case to fit everything inside
