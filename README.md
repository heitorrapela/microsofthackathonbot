# Microsoft Hackathon Bot-ando a mão na massa

Repository of the winning project of Microsoft Hackathon "Bot-ando a mão na massa" that occurred in the CIn/UFPE with two hours of duration. In the Microsoft Hackathon "Bot-ando a mão na massa", you could participate in solo or up to three people and you had to create your own bot using the Microsoft Bot Framework and with one of the following languages: C#, JavaScript, Python or Java.

The language chosen for development was python, as well as some libs of computer vision (OpenCV), face detection (dlib), and pygame (audio).

For Hackathon we did a chatbot project to take care of babies with the following functionalities:
1) Check the state of the baby
2) Check the environment in real time
3) Play a song for the baby to sleep
4) Turn off the song

## Installation steps (conda env):

    conda env create -f mshack.yml
    conda activate mshack
    /home/$USER/anaconda2/envs/mshack/bin/pip install yarl==0.7.1
    /home/$USER/anaconda2/envs/mshack/bin/pip install aiohttp==3.1

    Now, you need to run .sh script to install botbuilder-python:
    sudo chmod +x pip_install.sh
    ./pip_install.sh

## Testing if the install was succesfull:
    
    pytest

## Run code:
    
    conda activate mshack
    python main.py
    ./emulator/BotFramework-Emulator-4.3.3-linux-x86_64.AppImage

## References

[Botbuilder-Python](https://github.com/Microsoft/botbuilder-python) 
[Botbuilder-Samples](https://github.com/Microsoft/BotBuilder-Samples/blob/master/README.md)
[UFPE News](https://www.ufpe.br/agencia/noticias/-/asset_publisher/VQX2pzmP0mP4/content/microsoft-realiza-recrutamento-no-centro-de-informatica/40615)

### Please Feel Free to Contact Us!

**Heitor Rapela** ([GitHub :octocat:](https://github.com/heitorrapela))
  
![](https://github.com/heitorrapela.png?size=230)  
**hrm@cin.ufpe.br**

**Renie de Azevedo** ([GitHub :octocat:](https://github.com/R3NI3))
  
![](https://github.com/R3NI3.png?size=230)  
**rad@cin.ufpe.br**

**Carlos Pena** ([GitHub :octocat:](https://github.com/CarlosPena00))
  
![](https://github.com/CarlosPena00.png?size=230)  
**chcp@cin.ufpe.br**