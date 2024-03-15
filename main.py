import requests
from fastapi import FastAPI

app = FastAPI()
header ={ "Content-Type": "application/json",
          "Authorization": "Bearer sk_prod_TfMbARhdgues5AuIosvvdAC9WsA5kXiZlW8HZPaRDlIbCpSpLsXBeZO7dCVZQwHAY3P4VSBPiiC33poZ1tdUj2ljOzdTCCOSpUZ_3912"}
r = requests.get(" https://api.fillout.com/v1/api/forms/cLZojxk94ous",headers=header)

@app.get("/")
async def root():
    return {"message": "Data Filter"}

@app.get("/{formId}/filteredResponses")
def filterResponse(formId:str, filters , limit: str | None = 150):
    try:
        fomr_data = requests.get(" https://api.fillout.com/v1/api/forms/"+formId+"/submissions",headers=header)
    except:
        return {'error': 'form not found'}
    
    
    responses = fomr_data.json()['responses']
    result_submissions = []
    for submission in responses:
        if (filter_submission(submission['questions'],filters)):
            result_submissions.append(submission)
    return {'pageCount': (len(result_submissions)//limit+1),'responses':result_submissions,'totalResponses': len(result_submissions)}
 
        
    # for questios in responses:
        
    
def filter_submission(questions:list,filters:list)->bool:
    for question in questions:
        for filter in filters:
            if filter['id'] == question['id']:
                if (not apply_filter(question['value'],filter['value'],filter['condition'])):
                    return False
    return True
                

def apply_filter(val_1,val_2,filter:str)->bool:
    if filter == 'equals':
        return val_1 == val_2
    elif filter =='does_not_equal':
        return val_1 != val_1
    elif filter == 'greater_than':
        return val_1 > val_2
    elif filter == 'less_than':
        return val_1 < val_2
    else:
        return True
        
        
        
    

    
    
    
   