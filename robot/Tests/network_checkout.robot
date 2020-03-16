*** Settings ***
Documentation
Library  SSHLibrary
Suite Setup  Open Connection And Log In
Suite Teardown  Close All Connections

*** Variables ***
${HOST}     192.168.11.1
${USERNAME}     Cisco
${PASSWORD}     Cisco


*** Keywords ***
Open Connection And Log In
    [Documentation]  A ping can be sent from R1 to R2
    open connection  ${HOST}
    login   ${USERNAME}     ${PASSWORD}

Close All Connections
    [Documentation]  All connections are closed at the end of the test
    close connection  ${HOST}

*** Test Cases ***
R1 can ping R2
[Documentation] R1 (192.168.12.1) can ping it's R2 (192.168.12.2)
${output}= Execute Commmand ping 192.168.13.1 -c 1
Should Contain ${output} 64 bytes frin 192.168.13.1
