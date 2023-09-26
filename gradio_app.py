import gradio as gr
import prodia_image_gen as pr


def generate_image(model,promt,negative_prompt,aspect_ratio,steps,cfg_scale,seed,upscale,sampler):
    return pr.generate_gradio(model,promt,negative_prompt,aspect_ratio,steps,cfg_scale,seed,upscale,sampler),pr.galimg


model = gr.Dropdown(choices=pr.models,value="Realistic_Vision_V5.0.safetensors [614d1063]",label="Model",info="Choose the model to generate the image",scale=1)
aspect_ratio = gr.Dropdown(["square","portrait","landscape"], label="Aspect Ratio",value="square",info="Choose the aspect ratio of the image",scale=1)
promt = gr.Textbox(lines=2,max_lines=50,label="Prompt",placeholder="Enter the prompt here",info="Enter the prompt to generate the image",scale=1)
negative_prompt = gr.Textbox(lines=2,max_lines=20,value="",label="Negative Prompt",placeholder="Enter the negative prompt here",info='Enter things you don\'t want to include.(optional)',scale=1)
steps = gr.Slider(minimum=1,maximum=100,label="Steps",value=25,step=1,info="Number of steps to run the model",scale=1)
cfg_scale = gr.Slider(minimum=1,maximum=10,label="CFG Scale",value=7,step=1,info="CFG Scale",scale=1)
seed = gr.Slider(minimum=-1,maximum=100,label="Seed",value=-1,step=1,info="Seed",scale=1)
upscale = gr.Checkbox(label="Upscale",value=False,info="Upscale the image",scale=1)
sampler = gr.Dropdown(choices=pr.sampler,label="Sampler",value="DPM++ 2M Karras",info="Choose the sampler",scale=1)


gr.Interface(fn=generate_image,
             inputs=[model,promt,negative_prompt,aspect_ratio,steps,cfg_scale,seed,upscale,sampler],
             outputs=["image",gr.Gallery(pr.galimg,
                                         label="Example output Images",show_label=True,height="700px",columns=3,preview=False,show_share_button=True)],title="ImagTo",description="Let you imagination speak. Type what's on your mind and see the magic happen.",
                                         examples=[[pr.models[34],pr.ex_prompt1,pr.ex_nprompt1,"landscape",25,7,-1,False,"DPM++ 2M Karras"],[pr.models[34],pr.ex_prompt2,pr.ex_nprompt2,"landscape",25,7,-1,False,"DPM++ 2M Karras"],
                                                   [pr.models[16],pr.ex_prompt3,pr.ex_nprompt3,"landscape",25,7,-1,False,"DPM++ 2M Karras"],[pr.models[18],pr.ex_prompt4,pr.ex_nprompt4,"landscape",25,7,-1,False,"DPM++ 2M Karras"]],
                                         article="MADE BY VIGNESH [Follow mw on LinkedIn](https://www.linkedin.com/in/vignesh-m20)").queue(concurrency_count=50,max_size=50).launch(show_api=False)



