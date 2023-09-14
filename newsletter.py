import csv

def filter_subscriber(subscribers_file, email, blacklist):
  filtered_subscriber = []
  blacklist_names = []

  with open(blacklist, 'r') as blacklist_csv:
      blacklist_reader = csv.reader(blacklist_csv, delimiter=';')
      blacklist_names = [row[0].strip() for row in blacklist_reader]

  with open(subscribers_file, 'r') as subscribers_csv:
    subscribers_reader = csv.reader(subscribers_csv, delimiter=';')
    for subscriber in subscribers_reader:
      subscriber_email = subscriber[1].strip()
      subscriber_name = subscriber[0].strip()
      if email in subscriber_email:
        if subscriber_name not in blacklist_names: 
          filtered_subscriber.append(subscriber)

  return filtered_subscriber

def filter_forwarding_emails(forwarding_file, filtered_subscribers):
  subscriber_emails = set()
  filtered_forwards = []
  left = []

  for row in filtered_subscribers:
    subscriber_email = row[1].strip()
    subscriber_emails.add(subscriber_email)

  with open(forwarding_file, 'r') as forwarding_csv:
    forwarding_reader = csv.reader(forwarding_csv, delimiter=';')
    for row in forwarding_reader:
      forwarding_email = row[0].strip()
      forwarding_target = row[1].strip()
      if forwarding_email in subscriber_emails:
        filtered_forwards.append((forwarding_email, forwarding_target))
      else:
        left.append((forwarding_email, forwarding_target))

  return filtered_forwards

def replace_subscriber_emails(filtered_subscribers, filtered_forwards, subscribers_file):
  replaced_subscriber_data = []
  unfiltered_subscribers_emails = []
  replaced_subscriber_email = []

  with open(subscribers_file, 'r') as subscribers_csv:
    subscribers_reader = csv.reader(subscribers_csv, delimiter=';')
    unfiltered_subscribers_emails = [row[1].strip() for row in subscribers_reader]

  for row in filtered_subscribers:
    subscriber_name = row[0].strip()
    subscriber_email = row[1].strip()
    subscriber_data = row[2:] 
    for forwarding_email, forwarding_target in filtered_forwards:
      if subscriber_email == forwarding_email:
        if forwarding_target not in unfiltered_subscribers_emails:
          if forwarding_target not in replaced_subscriber_email:
              subscriber_data.insert(0, subscriber_name)
              subscriber_data.insert(1, forwarding_target)
              replaced_subscriber_data.append(subscriber_data)
              replaced_subscriber_email.append(forwarding_target)
          break
        break
    else:
      replaced_subscriber_data.append(row)

  return replaced_subscriber_data

def write_replaced_data_to_csv(output_file, replaced_data):
  with open(output_file, 'w', newline='') as output_csv:
    csv_writer = csv.writer(output_csv, delimiter=';')
    csv_writer.writerows(replaced_data)

if __name__ == "__main__":
  subscribers_file = "newsletter.csv"
  forwarding_file = "mailforwards.csv"
  subscriber_filtered = "subscriber_filtered.csv"
  output_file = "new_newsletter.csv"
  blacklist = "blacklist.csv"
  email = "@swv-sindelfingen.de"

  filtered_subscribers = filter_subscriber(subscribers_file, email, blacklist)
  filtered_forwards = filter_forwarding_emails(forwarding_file, filtered_subscribers)
  replaced_data = replace_subscriber_emails(filtered_subscribers, filtered_forwards, subscribers_file)
  write_replaced_data_to_csv(subscriber_filtered, filtered_subscribers)
  write_replaced_data_to_csv(output_file, replaced_data)

  print("Ersetzung abgeschlossen. Ergebnisse in", output_file)
