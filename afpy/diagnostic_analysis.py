print("This program returns prevalence, sensitivity, specificity, positive predictive value, and negative predictive value.")
tp = ""
tn = ""
fp = ""
fn = ""

def get_diagnostic_parameter_from_user(parameter, message:str):
    while type(parameter) != int:
        parameter = input(message)
        try:
            parameter = int(parameter)
        except:
            print("Only integer values can be accepted.")
    return parameter
    

tp = get_diagnostic_parameter_from_user(tp, "True positives: ")
tn = get_diagnostic_parameter_from_user(tn, "True negatives: ")
fp = get_diagnostic_parameter_from_user(fp, "False positives: ")
fn = get_diagnostic_parameter_from_user(fn, "False negatives: ")

try:
    prevalence = (tp+fn)/(tp+tn+fp+fn)
except:
    prevalence = 0
try:
    sensitivity = tp/(tp+fn)*100
except:
    sensitivity = 0
try:
    specificity = tn/(tn+fp)*100
except:
    specificity = 0
try:
    ppv = tp/(tp+fp)*100
except:
    ppv = 0
try:
    npv = tn/(tn+fn)*100
except:
    npv = 0

print(f"Prevalence: {prevalence}%")
print(f"Sensitivity: {sensitivity}%")
print(f"Specificity: {specificity}%")
print(f"Positive Predictive Value: {ppv}%")
print(f"Negative Predictive Value: {npv}%")