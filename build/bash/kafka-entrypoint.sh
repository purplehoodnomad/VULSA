set -e

if [ ! -f /var/lib/kafka/data/meta.properties ]; then
  echo 'Formatting KRaft storage...'
  CLUSTER_ID=$(/usr/bin/kafka-storage random-uuid)
  export CLUSTER_ID
  /usr/bin/kafka-storage format --cluster-id $CLUSTER_ID -t /var/lib/kafka/data
else
  # Extract cluster ID from existing meta.properties
  CLUSTER_ID=$(awk -F= '/cluster.id/ {print $2}' /var/lib/kafka/data/meta.properties)
  export CLUSTER_ID
fi

exec /etc/confluent/docker/run