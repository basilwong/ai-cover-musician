# ai-cover-musician

Note if you just wanna check out the output check out:

Sound Cloud: https://soundcloud.com/ai-music-covers

YouTube: https://www.youtube.com/channel/UC1L1IyK0OJHqMtY6ttXtvCw?view_as=subscriber

1. Fork the repository and clone it into AWS Sagemaker as a New Notebook Instance.
2. Go through main.ipynb file in the repository. Execute all the code blocks. 
3. The created files now need to be committed to the forked repository. 
4. The forked repository should then be cloned onto an Ubuntu machine. That way it is easy to satisfy the ffmpeg dependency with [sudo apt-get install ffmpeg]. 
5. Create a conda environment with the yml file in the repository. 
6. Activate the environment. 
7. Run [python main.py] from the root of the repo.
8. The final output will show up in the final-output folder of the repo.
