*** Settings ***
Library         DateTime
Library         OperatingSystem
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

Read my files absolute
    @{files_in_inputs}=   List Files In Directory   folder_inputs   absolute=True
    FOR  ${k}  IN  @{files_in_inputs}
         Log     ${k}   console=True
         ${cont}=   Get File    ${k}
         Log   ${cont}   console=True
    END

Read my files relative
    @{files_in_inputs}=   List Files In Directory   folder_inputs   absolute=False
    FOR  ${k2}  IN  @{files_in_inputs}
         Log   folder_inputs${/}${k2}   console=True
         ${cont2}=   Get File    folder_inputs${/}${k2}
         Log   ${cont2}   console=True
    END

Read my files absolute in subdirectories only (nested loop not subbport in Robot 3, but only from Robot 4 - so use keyword inside)
    @{directories}    List Directories In Directory    folder_inputs   absolute=True
    FOR  ${dir}  IN  @{directories}   # loop thorugh dir (since 'List Files In Directory' is not recursive)
        @{files_in_inputs}=   List Files In Directory   ${dir}   absolute=True
    END

Test tag to disable a test
    # [Tags]   some_tags_no_used    # if master is run with default tags
    Pass Execution    test temporarily disabled  # how to disable a test with a BuiltIn keyword
    Log   This test does run!    console=True
    Should Be True  3 == 3
    Should Be True  1 == 3  # fail


*** Keywords ***
setup my variables
    #{previous_wednesday}    Get Previous Wednesday
    #Set Suite Variable      ${previous_wednesday}
    ${previous_wednesday_2}  Get Previous Week Wednesday from date   # 2021-03-08
    Set Suite Variable       ${previous_wednesday_2}


Get Previous Week Wednesday from date
    [Arguments]         ${a_date}=${EMPTY}
    ${current_dt} =     Get Current Date    result_format=datetime  # with result_format=%w Sunday is 0
    ${a_date_dt} =	    Set Variable If  '${a_date}' == '${EMPTY}'  ${current_dt}	${a_date}
    Log To Console      ${a_date_dt}
    ${a_date_dt}        Convert Date        ${a_date_dt}    result_format=datetime
    ${week_day}         Evaluate            $a_date_dt.weekday()       # Monday is 0
    Log To Console      day of the week: ${week_day}
    ${days_past_Wed}    Evaluate            ${week_day} + 4 + 1  # excludes current Wednesday, weekday+6-wd+1
    ${prev_Wed}         Subtract Time From Date     ${a_date_dt}    ${days_past_Wed} days    result_format=datetime
    [Return]            ${prev_Wed}

Get Previous Wednesday from date
    [Arguments]         ${a_date}=${EMPTY}
    ${current_dt} =     Get Current Date    result_format=datetime  # with result_format=%w Sunday is 0
    ${a_date_dt} =	    Set Variable If  '${a_date}' == '${EMPTY}'  ${current_dt}	${a_date}
    Log To Console      ${a_date_dt}
    ${a_date_dt}        Convert Date        ${a_date_dt}    result_format=datetime
    ${week_day}         Evaluate            $a_date_dt.weekday()       # Monday is 0
    ${days_past_Wed}    Evaluate            ${week_day} + 4 + 1  # excludes current Wednesday, weekday+6-wd+1
    ${prev_Wed}         Subtract Time From Date     ${a_date_dt}    ${days_past_Wed}   days    result_format=datetime
    [Return]            ${prev_Wed}

Loop insie
    [Arguments]         ${a_date}=${EMPTY}
    FOR  ${k}  IN  @{files_in_inputs}
         Log     ${k}   console=True
         ${cont}=   Get File    ${k}
         Log   ${cont}   console=True
    END
