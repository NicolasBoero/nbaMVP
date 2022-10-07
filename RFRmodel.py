import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

final = pd.read_csv('final.csv', sep = ';')
final = pd.concat([final , final['Pos'].str.get_dummies()], axis = 1)

lst_result = []

for year in range(1980, 2023):
    pred = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
       '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'FOULS', 'PTS', 'year',
       'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%',
       'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM',
       'BPM', 'VORP', 'W', 'L', 'W/L%', 'GMissed%', 'C', 'PF', 'PG',
       'SF', 'SG']

    train = final[final['year'] < year]
    test = final[final['year'] == year]

    modelRFC = RandomForestRegressor(random_state = 42)
    modelRFC.fit(train[pred], train['Share'])

    train_score = modelRFC.score(train[pred], train['Share'])
    test_score = modelRFC.score(test[pred], test['Share'])

    predictions = pd.DataFrame(modelRFC.predict(test[pred]), columns = ["prediction"], index = test.index)
    model_result = pd.concat([test[["Player", "Share"]], predictions], axis =1).sort_values(by ='Share', ascending = False)
    model_result = model_result.sort_values('Share', ascending = False)
    model_result['actual_rank'] = list(range(1, model_result.shape[0]+1))
    model_result = model_result.sort_values('prediction', ascending = False)
    model_result['predicted_rank'] = list(range(1, model_result.shape[0]+1))
    model_result['year'] = year
    lst_result.append(model_result)
  
# TO SEE ONLY THE MVPs

#    mvp_result = model_result[model_result['actual_rank'] == 1].copy()
#    mvp_result['right_pred?'] = mvp_result.apply(lambda x : 'yes' if x['actual_rank'] == x['predicted_rank'] else 'no', axis = 1) 
#    mvp_result['year'] = year
#    mvp_result['train_score'] = round(train_score, 3)
#    mvp_result['test_score'] = round(test_score, 3)
#    lst_result.append(mvp_result)

    
lst_result = pd.concat(lst_result)
print(lst_result)

# print(lst_result['right_pred?'].value_counts(normalize = True))

# lst_result.to_excel('mvp_results.xlsx')
