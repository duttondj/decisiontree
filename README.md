# decisiontree
## Background
A decision tree is a flowchart-like structure in which each internal node represents a "test" on an attribute (e.g. whether a coin flip comes up heads or tails), each branch represents the outcome of the test and each leaf node represents a class label (decision taken after computing all attributes). The paths from root to leaf represents classification rules.

## Usage
Training data along with a list of attributes with possible values are taken in by `train()` to create a decision tree. This will produce a formated textfile containing the decision tree. It will not contain all attributes, only those necessary to make a decision based on input data.

The attributes file should resemble the below:
```
Alternate, Yes, No
Bar, Yes, No
Fri/Sat, Yes, No
Hungry, Yes, No
Patrons, None, Some, Full
Price, $, $$, $$$
Raining, Yes, No
Reservation, Yes, No
Type, French, Italian, Thai, Burger
WaitEstimate, 0-10, 10-30, 30-60, >60
ClassLabel, Yes, No
```
It contains an attribute followed by the possible values for it. The actual result should be the last item in the list.

Training data is the list of values cooresponding to the list of attributes. This data is what is actually used to create the decision tree in `train()`. The format is below:

```
Yes, No,  No,  Yes, Some, $$$, No,   Yes, French,  0-10,   Yes
Yes, No,  No,  Yes, Full, $,   No,   No,  Thai,    30-60,  No
No,  Yes, No,  No,  Some, $,   No,   No,  Burger,  0-10,   Yes
Yes, No,  Yes, Yes, Full, $,   No,   No,  Thai,    10-30,  Yes
Yes, No,  Yes, No,  Full, $$$, No,   Yes, French,  >60,    No 
No,  Yes, No,  Yes, Some, $$,  Yes,  Yes, Italian, 0-10,   Yes
No,  Yes, No,  No,  None, $,   Yes,  No,  Burger,  0-10,   No
No,  No,  No,  Yes, Some, $$,  Yes,  Yes, Thai,    0-10,   Yes
No,  Yes, Yes, No,  Full, $,   Yes,  No,  Burger,  >60,    No 
Yes, Yes, Yes, Yes, Full, $$$, No,   Yes, Italian, 10-30,  No 
No,  No,  No,  No,  None, $,   No,   No,  Thai,    0-10,   No 
Yes, Yes, Yes, Yes, Full, $,   No,   No,  Burger,  30-60,  Yes
```

The outputed decision tree follows the below format:

```
Test Patrons
 Patrons = None ==> RESULT = No
 Patrons = Full ==> Test Type
     Type = Burger ==> Test Raining
         Raining = Yes ==> RESULT = No
         Raining = No ==> RESULT = Yes
     Type = Thai ==> Test WaitEstimate
         WaitEstimate = 10-30 ==> RESULT = Yes
         WaitEstimate = 30-60 ==> RESULT = No
         WaitEstimate = 0-10 ==> RESULT = Yes
         WaitEstimate = >60 ==> RESULT = Yes
     Type = French ==> RESULT = No
     Type = Italian ==> RESULT = No
 Patrons = Some ==> RESULT = Yes
```

The `predict()` function uses a decision tree created by `train()` along with an attribute file and an input data file which contains lists of inputs to the attributes. It does not require the final class level attribute value but if its there, a user can visually compare the predicted response with a known response. The function will output the input data with a class level at the end of each line.

The `cross_validation()` function takes in similar parameters as `train()` does but the user can also specifiy the number of k-folds (default=10) in the test along with the number of trials to be done (default=1). This function will build the decision tree using the attributes file and training data and will then test the tree. The returned value is a metric between 0 and 1 for how good at predicting a result a tree is, higher is better. A higher metric can be obtained by having more training data, a tree is only as good as the variety of data it is given. More trials can produce a more exact metric as they are averaged over the number of trials.

Additionally, the training data and input data files can use 'N/A' as a value where any of the possible values for that attribute are used to create the tree. This may create very large and complex trees.
