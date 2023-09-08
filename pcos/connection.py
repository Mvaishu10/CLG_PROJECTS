import pickle
import pandas as pd

final_cosine_sim = pickle.load(open('final_cosine_sim.pkl','rb'))
indices = pickle.load(open('indices.pkl','rb'))
zomato_df = pickle.load(open('PCOS_df.pkl','rb'))
top_rest = pickle.load(open('pcos.pkl', 'rb'))


def similar_rests(name, cosine_similarities = final_cosine_sim):
    
    # Create a list to put top restaurants
    PCOS_exist = []
    
    # Find the index of the hotel entered
    idx = indices[indices == name].index[0]
    
    # Find the restaurants with a similar cosine-sim value and order them from bigges number
    score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)
    
    # Extract top  indexes with a similar cosine-sim value
    top30_indexes = list(score_series.iloc[0:31].index)
    
    # Names of the top 
    for each in top30_indexes:
        recommend_restaurant.append(list(zomato_df.index)[each])
    
    # Creating the new data set to show similar restaurants
    df_new = pd.DataFrame(columns=['cuisines', 'Mean Rating', 'cost'])
    
    # Create the top 30 similar restaurants with some of their columns
    for each in recommend_restaurant:
        df_new = pd.concat([df_new, pd.DataFrame(zomato_df[['cuisines','Mean Rating', 'cost']][zomato_df.index == each].sample())])
    
    # Drop the same named restaurants and sort only the top 10 by the highest rating
    df_new = df_new.drop_duplicates(subset=['cuisines','Mean Rating', 'cost'], keep=False)
    df_new = df_new.sort_values(by='Mean Rating', ascending=False).head(15)
    df_new.reset_index(names='name', inplace=True)
        
    return df_new.to_json(orient='records') 


def get_top_rests():
    rests = top_rest.head(30)
    print(rests.shape)
    return rests.to_json(orient='records')