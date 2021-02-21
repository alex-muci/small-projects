*** Settings ***
Library         DateTime
Documentation   Test some rolling dates
Suite Setup     setup my variables

*** Variables ***
${test_date}        Convert Date        2021-01-11 23:00    result_format=datetime

*** Test Cases ***
Let me test if Get Previous Wednesday works from date
    ${test_date} =     Get Current Date
    ${type string}=    Evaluate     type($test_date)
    Log To Console     ${type string}
    #Log To Console     ${previous_wednesday}
    Log To Console     ${previous_wednesday_2}



*** Keywords ***
setup my variables
    #{previous_wednesday}    Get Previous Wednesday
    #Set Suite Variable      ${previous_wednesday}
    ${previous_wednesday_2}  Get Previous Wednesday from date   # 2021-01-11
    Set Suite Variable       ${previous_wednesday_2}


Get Previous Wednesday from date
    [Arguments]         ${a_date}=${EMPTY}
    ${current_dt} =     Get Current Date    result_format=datetime
    ${a_date_dt} =	    Set Variable If  '${a_date}' == '${EMPTY}'  ${current_dt}	${a_date}
    Log To Console      ${a_date_dt}
    ${a_date_dt}        Convert Date        ${a_date_dt}    result_format=datetime
    ${week_day}         Evaluate            $a_date_dt.weekday()       # Monday is 0
    Log To Console     ${week_day}
    ${days_past_Wed}    Evaluate            ${week_day} + 4 + 1  # excludes current Wednesday, weekday+6-wd+1
    ${prev_Wed}         Subtract Time From Date     ${a_date_dt}    ${days_past_Wed} days    result_format=datetime
    [Return]            ${prev_Wed}
