from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime
from collections import defaultdict
import time

class KafkaStreamProcessor:
    def __init__(self):
        # Initializing tracking metrics
        self.device_stats = defaultdict(int)
        self.version_stats = defaultdict(int)
        self.locale_stats = defaultdict(int)
        self.messages_processed = 0
        self.unique_users = set()
        self.data_quality_issues = defaultdict(int)
        self.timestamp_issues = defaultdict(int)
        self.start_time = time.time()

    def validate_and_transform_data(self, data):
        """
        Validating and transforming incoming data with enhanced quality checks
        relevant to user login patterns and app usage
        """
        try:
            field_defaults = {
                'user_id': 'unknown_user',
                'app_version': '0.0.0',
                'device_type': 'unknown_device',
                'ip': '0.0.0.0',
                'locale': 'unknown_locale',
                'device_id': 'unknown_device_id',
                'timestamp': str(int(datetime.now().timestamp()))
            }
            # Validating and tracking data quality
            for field, default_value in field_defaults.items():
                if field not in data or not data[field]:
                    self.data_quality_issues[f'missing_{field}'] += 1
                    data[field] = default_value

            # Normalizing device type for consistent analytics
            data['device_type'] = self.normalize_device_type(data.get('device_type', ''))
            
            # Validating timestamp and tracking temporal issues
            try:
                timestamp = int(data['timestamp'])
                current_time = int(time.time())
                if timestamp > current_time:
                    self.timestamp_issues['future'] += 1
                data['datetime'] = datetime.fromtimestamp(timestamp).isoformat()
            except (ValueError, TypeError):
                self.timestamp_issues['invalid'] += 1
                data['datetime'] = datetime.now().isoformat()
                data['timestamp'] = str(int(time.time()))

            return data

        except Exception as e:
            print(f"Error in data validation: {str(e)}")
            return None

    def normalize_device_type(self, device_type):
        """Normalizes device types for consistent tracking"""
        if not device_type:
            return 'unknown_device'
            
        device_mapping = {
            'ios': 'iOS',
            'android': 'android'
        }
        return device_mapping.get(device_type.lower(), 'unknown_device')

    def mask_ip(self, ip):
        """Masks IP address for privacy"""
        try:
            octets = ip.split('.')
            return f"{octets[0]}.{octets[1]}.{octets[2]}.xxx"
        except:
            return "invalid.ip.xxx"

    def process_message(self, message):
        """
        Processing individual messages with business-relevant transformations
        and tracking metrics
        """
        try:
            data = message.value
            validated_data = self.validate_and_transform_data(data)
            if not validated_data:
                return None

            # Updating analytics counters
            self.messages_processed += 1
            self.unique_users.add(validated_data['user_id'])
            self.device_stats[validated_data['device_type']] += 1
            self.version_stats[validated_data['app_version']] += 1
            self.locale_stats[validated_data['locale']] += 1

            # Transforming data
            processed_data = {
                **validated_data,
                'masked_ip': self.mask_ip(validated_data['ip']),
                'processed_at': datetime.now().isoformat(),
                'version_category': self.categorize_version(validated_data['app_version'])
            }

            # Printing insights periodically
            if self.messages_processed % 100 == 0:
                self.print_insights()

            return json.dumps(processed_data).encode('utf-8')

        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return None

    def categorize_version(self, version):
        """Categorizing app versions for version adoption analysis"""
        try:
            major, minor = map(int, version.split('.')[:2])
            if major < 2:
                return 'legacy'
            elif major == 2 and minor < 3:
                return 'stable'
            return 'current'
        except:
            return 'invalid'

    def print_insights(self):
        """
        Print comprehensive insights about user behavior, app usage,
        and data quality metrics
        """
        print("\n=== Real-time Insights ===")
        
        # User Engagement Metrics
        print("\n1. User Engagement:")
        print(f"Total Messages Processed: {self.messages_processed}")
        print(f"Unique Users: {len(self.unique_users)}")
        print(f"Messages/Second: {self.messages_processed/(time.time()-self.start_time):.2f}")

        # Device Distribution
        print("\n2. Platform Analytics:")
        total_devices = sum(self.device_stats.values())
        for device, count in self.device_stats.items():
            percentage = (count/total_devices) * 100
            print(f"{device}: {percentage:.1f}%")

        # Version Distribution
        print("\n3. App Version Adoption:")
        total_versions = sum(self.version_stats.values())
        latest_version_users = self.version_stats.get('2.3.0', 0)
        print(f"Latest Version (2.3.0) Adoption: {(latest_version_users/total_versions)*100:.1f}%")

        # Geographic Distribution
        print("\n4. Geographic Distribution:")
        top_locales = sorted(self.locale_stats.items(), key=lambda x: x[1], reverse=True)[:3]
        for locale, count in top_locales:
            percentage = (count/self.messages_processed) * 100
            print(f"{locale}: {percentage:.1f}%")

        # Data Quality Metrics
        if self.data_quality_issues:
            print("\n5. Data Quality Summary:")
            for issue, count in self.data_quality_issues.items():
                percentage = (count/self.messages_processed) * 100
                print(f"{issue}: {count} occurrences ({percentage:.1f}%)")

def main():
    """Main function to run the Kafka consumer"""
    processor = KafkaStreamProcessor()
    
    # Initializing Kafka consumer
    consumer = KafkaConsumer(
        'user-login',
        bootstrap_servers=['localhost:29092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='login-processor-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        session_timeout_ms=30000,
        heartbeat_interval_ms=10000
    )

    # Initializing Kafka producer for processed data
    producer = KafkaProducer(
        bootstrap_servers=['localhost:29092'],
        value_serializer=lambda x: x,
        retries=3,
        acks='all'
    )

    print("Starting Kafka Stream Processor...")
    
    try:
        for message in consumer:
            processed_message = processor.process_message(message)
            if processed_message:
                producer.send('processed-user-login', value=processed_message)
                producer.flush()
    except KeyboardInterrupt:
        print("\nGracefully shutting down...")
    finally:
        consumer.close()
        producer.close()

if __name__ == "__main__":
    main()