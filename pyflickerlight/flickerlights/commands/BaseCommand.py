# class BaseCommand(object):
#     def __init__(self, timestamp, groupid = 0):
#         self.groupid = groupid
#         self.timestamp = timestamp
#
#     def to_message(self):
#         pass
#
# message Strobe {
#   required uint32 length = 1;
#   required uint32 rate = 2;
#   required uint32 on_color = 3;
#   optional uint32 off_color = 4;
# }
#
# message Fade {
#   required uint32 length = 1;
#   required uint32 dest_color = 2;
#   optional uint32 start_color = 3;
# }
#
# message SetColor {
#   required uint32 dest_color = 1;
# }
#
# message FlickerBaseMessage {
#   required uint32 groupid = 1;
#   required uint32 timestamp = 2;
#   oneof payload {
#     Strobe strobe = 3;
#     Fade fade = 4;
#     SetColor setColor = 5;
#   }
# }
