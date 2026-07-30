import json
import pandas as pd

class FewShotPosts:
    def __init__(self,FilePath="data/processed_posts.json"):
        self.df=None
        self.unique_tags=None
        self.load_posts(FilePath)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)

        # clean corrupted unicode characters
        for post in posts:
            if "text" in post:
                post["text"] = (
                    post["text"]
                    .encode("utf-16", "surrogatepass")
                    .decode("utf-16", "ignore")
                )



        self.df=pd.json_normalize(posts)
        self.df["length"]=self.df["line_count"].apply(self.categorize_length)
        # collect unique tags
        all_tags = self.df['tags'].apply(lambda x: x).sum()
        self.unique_tags = list(set(all_tags))




    def get_filtered_posts(self,length,language,tag):
       df_filtered= self.df[
           (self.df["length"]==length) &
           (self.df["language"]==language) &
           (self.df["tags"].apply(lambda tags:tag in tags))
       ]
       return df_filtered.to_dict(orient="records")

    def categorize_length(self,line_count):
        if line_count<5:
            return "short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else :
            return "Long"



    def get_tags(self):
        return self.unique_tags



if __name__ == "__main__":
    fs= FewShotPosts()
    posts= fs.get_filtered_posts("Medium","Hinglish","Job Search")
    fs.df.to_csv("posts.csv", index=False)