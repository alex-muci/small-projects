*** Settings ***
Library         REST
Documentation   Test data can be read from variables and files.
...             IMPORTANT, install it first: pip install --upgrade RESTinstance

*** Variables ***
${TEST_URL}     https://jsonplaceholder.typicode.com


*** Test Cases ***
Let me test if I can get the value
    ${resp_body}=       GET an existing user, notice how the schema gets more accurate
    # ${here}=   Catenate    SEPARATOR=---   Hello   ${here}
    #
    Object              $.address.geo           # NB: we can test, but not save this into variable
    String              $.address.geo.lat
    Log to Console      ${resp_body.keys()}  # this is a dictionary
    #
    ${dict_to_json}=    evaluate   json.dumps(${resp_body}, indent=4)  json
    ${json_to_dict}=    evaluate   json.loads('''${dict_to_json}''')   json
    #
    ${latitude}=        Convert To Number  ${json_to_dict['address']['geo']['lat']}
    Should Be True	    ${latitude}!=10
    Log to Console      ${json_to_dict['name']}


*** Keywords ***
Get Bond data
    [Arguments]     ${json_data}
    # users/4
    ${json}=    evaluate    json.loads('''${json_data}''')    json
    # ${invoice_id}=   Convert To String   ${invoice["id"]}
    [return]  ${json}

GET an existing user, notice how the schema gets more accurate
    GET         ${TEST_URL}/users/1                  # this creates a new instance
    # Output schema   response body
    Object      response body             # values are fully optional
    Integer     response body id          1
    String      response body name        Leanne Graham
    # Output      response body           # NB if no file specified, then print on terminal
    # ${test}=    Output     $.name
    ${res}=   Output    response body  ${EXECDIR}/my_test.json
    # Log to Console      ${json_res}
    [Return]    ${res}
    # [Teardown]  Output schema

GET existing users, use JSONPath for very short but powerful queries
    GET         ${TEST_URL}/users?_limit=5           # further assertions are to this
    Array       response body
    Integer     $[0].id                   1           # first id is 1
    String      $[0]..lat                 -37.3159    # any matching child
    Integer     $..id                     maximum=5   # multiple matches
    # [Teardown]  Output  $[*].email        # outputs all emails as an array
