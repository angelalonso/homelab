set -euo pipefail

SECRETS="db_feed_name \
  db_feed_user \
  db_feed_pass \
  "
for secret in ${SECRETS}; do
  secretvalue=''
  echo $secret
  while [[ $secretvalue == '' ]]; do
    if [[ $secret == *"pass"* ]]; then
      stty -echo
      read -p "Enter a valid value for: $secret ->" secretvalue # Ask the user to enter a string
      stty echo
    else
      read -p "Enter a valid value for: $secret ->" secretvalue # Ask the user to enter a string
    fi
  done 
  echo "$secretvalue" | docker secret create $secret -
done
