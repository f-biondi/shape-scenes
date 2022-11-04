import os 
import openai
import time
api_key='#Insert your api'
openai.api_key= (api_key)
try:
    for i in range(0,24474):
        namefile= "res/prompts/"+str(i)+".txt"
        textfile = open(namefile, "r")
        testo= textfile.read()
        textfile.close()
        gpt_prompt= "rewrite the following sentence in 4 different ways while maintaining the same meaning \n\n "+"A 3d render of "+ str(testo)+ "\n-"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=gpt_prompt,
            temperature=0.5,
            max_tokens=750,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        text=response['choices'][0]['text']
        print(i)
        p=text.split("\n")
        a=1
        for x,phrases in enumerate(p):
            path= "res/prompts2/"+str(i)+"_"+str(a)+".txt"
            text_file=open(path,"w")
            if(phrases[0]=="-"):
                text_file.write(phrases[1:])
                a+=1

            else:
                text_file.write(phrases)
                a+=1
            if(a==4):
                break;
            text_file.close()
        path= "res/prompts2/"+str(i)+"_0.txt"
        text_file=open(path,"w")
        text_file.write("A 3d render of "+str(testo))
        text_file.close()
        time.sleep(3)
except:
    print("Error in file number",i)
    exit(0)
