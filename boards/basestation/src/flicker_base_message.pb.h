/* Automatically generated nanopb header */
/* Generated by nanopb-0.3.7-dev at Sun Sep 11 22:07:26 2016. */

#ifndef PB_FLICKER_BASE_MESSAGE_PB_H_INCLUDED
#define PB_FLICKER_BASE_MESSAGE_PB_H_INCLUDED
#include <pb.h>

/* @@protoc_insertion_point(includes) */
#if PB_PROTO_HEADER_VERSION != 30
#error Regenerate this file with the current version of nanopb generator.
#endif

#ifdef __cplusplus
extern "C" {
#endif

/* Struct definitions */
typedef struct _Fade {
    uint32_t length;
    uint32_t dest_color;
    bool has_start_color;
    uint32_t start_color;
/* @@protoc_insertion_point(struct:Fade) */
} Fade;

typedef struct _SetColor {
    uint32_t dest_color;
/* @@protoc_insertion_point(struct:SetColor) */
} SetColor;

typedef struct _Strobe {
    uint32_t length;
    uint32_t rate;
    uint32_t on_color;
    bool has_off_color;
    uint32_t off_color;
/* @@protoc_insertion_point(struct:Strobe) */
} Strobe;

typedef struct _FlickerBaseMessage {
    uint32_t groupid;
    uint32_t timestamp;
    pb_size_t which_payload;
    union {
        Strobe strobe;
        Fade fade;
        SetColor setColor;
    } payload;
/* @@protoc_insertion_point(struct:FlickerBaseMessage) */
} FlickerBaseMessage;

/* Default values for struct fields */

/* Initializer values for message structs */
#define Strobe_init_default                      {0, 0, 0, false, 0}
#define Fade_init_default                        {0, 0, false, 0}
#define SetColor_init_default                    {0}
#define FlickerBaseMessage_init_default          {0, 0, 0, {Strobe_init_default}}
#define Strobe_init_zero                         {0, 0, 0, false, 0}
#define Fade_init_zero                           {0, 0, false, 0}
#define SetColor_init_zero                       {0}
#define FlickerBaseMessage_init_zero             {0, 0, 0, {Strobe_init_zero}}

/* Field tags (for use in manual encoding/decoding) */
#define Fade_length_tag                          1
#define Fade_dest_color_tag                      2
#define Fade_start_color_tag                     3
#define SetColor_dest_color_tag                  1
#define Strobe_length_tag                        1
#define Strobe_rate_tag                          2
#define Strobe_on_color_tag                      3
#define Strobe_off_color_tag                     4
#define FlickerBaseMessage_strobe_tag            3
#define FlickerBaseMessage_fade_tag              4
#define FlickerBaseMessage_setColor_tag          5
#define FlickerBaseMessage_groupid_tag           1
#define FlickerBaseMessage_timestamp_tag         2

/* Struct field encoding specification for nanopb */
extern const pb_field_t Strobe_fields[5];
extern const pb_field_t Fade_fields[4];
extern const pb_field_t SetColor_fields[2];
extern const pb_field_t FlickerBaseMessage_fields[6];

/* Maximum encoded size of messages (where known) */
#define Strobe_size                              24
#define Fade_size                                18
#define SetColor_size                            6
#define FlickerBaseMessage_size                  38

/* Message IDs (where set with "msgid" option) */
#ifdef PB_MSGID

#define FLICKER_BASE_MESSAGE_MESSAGES \


#endif

#ifdef __cplusplus
} /* extern "C" */
#endif
/* @@protoc_insertion_point(eof) */

#endif