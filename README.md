# aws-ses-serverless

## Bounce

If your recipient's receiver (for example, an ISP) fails to deliver your message to the recipient, the receiver 
bounces the message back to Amazon SES. Amazon SES then notifies you of the bounced email through email or through 
Amazon Simple Notification Service (Amazon SNS), depending on how you have your system set up. For more information,
 see Monitoring Using Amazon SES Notifications.
There are hard bounces and soft bounces, as follows:
Hard bounce – A persistent email delivery failure. For example, the mailbox does not exist. Amazon SES does not 
retry hard bounces, with the exception of DNS lookup failures. We strongly recommend that you do not make repeated 
delivery attempts to email addresses that hard bounce.
Soft bounce – A temporary email delivery failure. For example, the mailbox is full, there are too many connections 
(also called throttling), or the connection times out. Amazon SES retries soft bounces multiple times. If the email 
still cannot be delivered, then Amazon SES stops retrying it.
Amazon SES notifies you of hard bounces and soft bounces that will no longer be retried. However, only hard bounces 
count toward your bounce rate and the bounce metric that you retrieve using the Amazon SES console or the 
GetSendStatistics API.
Bounces can also be synchronous or asynchronous. A synchronous bounce occurs while the email servers of the sender and
receiver are actively communicating. An asynchronous bounce occurs when a receiver initially accepts an email message 
for delivery and then subsequently fails to deliver it to the recipient.


### Bounce Types
    
The following bounce types are available. 
We recommend that you remove the email addresses that have returned bounces marked Permanent from your mailing list,
as we do not believe that you will be able to successfully send to them in the future. Transient bounces are sent to
you when all retry attempts have been exhausted and will no longer be retried. You may be able to successfully 
resend to an address that initially resulted in a Transient bounce.    
    
| bounceType   | bounceSubType      | Description                                                                                                                                                                                                                                                        |
|--------------|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Undetermined | Undetermined       | Amazon SES was unable to determine a specific bounce reason.                                                                                                                                                                                                       |
| Permanent    | General            | Amazon SES received a general hard bounce and recommends that you remove the recipient's email address from your mailing list.                                                                                                                                     |
| Permanent    | NoEmail            | Amazon SES received a permanent hard bounce because the target email address does not exist. It is recommended that you remove that recipient from your mailing list.                                                                                              |
| Permanent    | Suppressed         | Amazon SES has suppressed sending to this address because it has a recent history of bouncing as an invalid address. For information about how to remove an address from the suppression list, see Removing an Email Address from the Amazon SES Suppression List. |
| Transient    | General            | Amazon SES received a general bounce. You may be able to successfully retry sending to that recipient in the future.                                                                                                                                               |
| Transient    | MailboxFull        | Amazon SES received a mailbox full bounce. You may be able to successfully retry sending to that recipient in the future.                                                                                                                                          |
| Transient    | MessageTooLarge    | Amazon SES received a message too large bounce. You may be able to successfully retry sending to that recipient if you reduce the message size.                                                                                                                    |
| Transient    | ContentRejected    | Amazon SES received a content rejected bounce. You may be able to successfully retry sending to that recipient if you change the message content                                                                                                                   |
| Transient    | AttachmentRejected | Amazon SES received an attachment rejected bounce. You may be able to successfully retry sending to that recipient if you remove or change the attachment.                                                                                                         |


    
## Complaint

Most email client programs provide a button labeled "Mark as Spam," or similar, which moves the message to a spam folder,
and forwards it to the ISP. Additionally, most ISPs maintain an abuse address (e.g., abuse@example.net), where users 
can forward unwanted email messages and request that the ISP take action to prevent them. In both of these cases, the 
recipient is making a complaint. If the ISP concludes that you are a spammer, and Amazon SES has a feedback loop set
up with the ISP, then the ISP will send the complaint back to Amazon SES. When Amazon SES receives such a complaint, 
it forwards the complaint to you either by email or by using an Amazon SNS notification, depending on how you have your
system set up. For more information, see Monitoring Using Amazon SES Notifications. We recommend that you do not make
repeated delivery attempts to email addresses that generate complaints.


You may see the following complaint types in the complaintFeedbackType field as assigned by the reporting ISP, according to the Internet Assigned Numbers Authority website:

* abuse - Indicates unsolicited email or some other kind of email abuse.
* auth-failure - Email authentication failure report.
* fraud - Indicates some kind of fraud or phishing activity.
* not-spam - Indicates that the entity providing the report does not consider the message to be spam. This may be used to correct a message that was incorrectly tagged or categorized as spam.
* other - Indicates any other feedback that does not fit into other registered types.
* virus - Reports that a virus is found in the originating message.


## Delivery

When the email is correctly delivered.

If happen something wrong that generate a Bounce or Complain but then we
receive a Delivery Object the system reset the bounce or complain fields of the delvered email.
