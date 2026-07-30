from urllib import response

from llm_helper import llm
from few_shot import FewShotPosts


few_shot= FewShotPosts()



def get_length_str(length):
    if length=="Short":
        return "1 to 5 lines"
    if length=='Medium':
        return "6 to 10 lines"
    if length=='Long':
        return "11 to 15 lines"





def get_prompt(length,language,tag):
    length_str=get_length_str(length)
    prompt = f'''
     Generate a linkedin post using the below information .No Preamble 
    1)Topic :{tag}
    2)Length:{length}
    3)Language:{language}
    '''
    # giving example for  user like content
    examples = few_shot.get_filtered_posts(length, language, tag)

    if (len(examples) > 0):
        prompt += "4) use the writing style as per the following examples"
        for i, post in enumerate(examples):
            post_text = post['text']
            prompt += "\n\n Examples{i} \n\n {post_text}"
            if i == 1:
                break

    return prompt

def generate_post(length,language,tag):
    prompt=get_prompt(length,language,tag)

    response = llm.invoke(prompt)
    return response.content


if __name__=="__main__":
    post = generate_post("Short","English","Job Search")
    print(post)