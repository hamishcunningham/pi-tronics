#!/bin/bash

# check to makre sure we’ve got the right number of arguments
if [[ $# -ne 2 ]]
then
	echo "$0 \"message\" phonenumber"
	echo "Phone number should have country code, no +"
	echo "Make sure this script has been edited for the correct BULKSMS username and password."
	exit 1
fi

# set character encoding, unknown if this is necessary
export LANG=en_GB.iso8859-1
export LC_ALL=en_GB.iso8859-1

# details
USERNAME="username"
PASSWORD="password"
MESSAGE="$1"
PHONE="$2"
DUPID=$[`date +%s` / $RANDOM]

# send the message
curl http://www.bulksms.co.uk/eapi/submission/send_sms/2/2.0 --data-urlencode stop_dup_id=$DUPID --data-urlencode username="$USERNAME" --data-urlencode password="$PASSWORD" --data-urlencode message="$MESSAGE" --data-urlencode msisdn="$PHONE"
