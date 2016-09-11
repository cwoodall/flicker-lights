/* Automatically generated nanopb constant definitions */
/* Generated by nanopb-0.3.7-dev at Sun Sep 11 15:17:53 2016. */

#include "led_basestation.pb.h"

/* @@protoc_insertion_point(includes) */
#if PB_PROTO_HEADER_VERSION != 30
#error Regenerate this file with the current version of nanopb generator.
#endif



const pb_field_t Flicker_fields[5] = {
    PB_FIELD(  1, UINT32  , REQUIRED, STATIC  , FIRST, Flicker, length, length, 0),
    PB_FIELD(  2, UINT32  , REQUIRED, STATIC  , OTHER, Flicker, rate, length, 0),
    PB_FIELD(  3, UINT32  , REQUIRED, STATIC  , OTHER, Flicker, on_color, rate, 0),
    PB_FIELD(  4, UINT32  , OPTIONAL, STATIC  , OTHER, Flicker, off_color, on_color, 0),
    PB_LAST_FIELD
};

const pb_field_t Fade_fields[4] = {
    PB_FIELD(  1, UINT32  , REQUIRED, STATIC  , FIRST, Fade, length, length, 0),
    PB_FIELD(  2, UINT32  , REQUIRED, STATIC  , OTHER, Fade, dest_color, length, 0),
    PB_FIELD(  3, UINT32  , OPTIONAL, STATIC  , OTHER, Fade, start_color, dest_color, 0),
    PB_LAST_FIELD
};

const pb_field_t SetColor_fields[2] = {
    PB_FIELD(  1, UINT32  , REQUIRED, STATIC  , FIRST, SetColor, dest_color, dest_color, 0),
    PB_LAST_FIELD
};

const pb_field_t Command_fields[6] = {
    PB_FIELD(  1, UINT32  , REQUIRED, STATIC  , FIRST, Command, groupid, groupid, 0),
    PB_FIELD(  2, UINT32  , REQUIRED, STATIC  , OTHER, Command, timestamp, groupid, 0),
    PB_ONEOF_FIELD(payload,   3, MESSAGE , ONEOF, STATIC  , OTHER, Command, flicker_command, timestamp, &Flicker_fields),
    PB_ONEOF_FIELD(payload,   4, MESSAGE , ONEOF, STATIC  , OTHER, Command, fade_command, timestamp, &Fade_fields),
    PB_ONEOF_FIELD(payload,   5, MESSAGE , ONEOF, STATIC  , OTHER, Command, set_color_command, timestamp, &SetColor_fields),
    PB_LAST_FIELD
};


/* Check that field information fits in pb_field_t */
#if !defined(PB_FIELD_32BIT)
/* If you get an error here, it means that you need to define PB_FIELD_32BIT
 * compile-time option. You can do that in pb.h or on compiler command line.
 * 
 * The reason you need to do this is that some of your messages contain tag
 * numbers or field sizes that are larger than what can fit in 8 or 16 bit
 * field descriptors.
 */
PB_STATIC_ASSERT((pb_membersize(Command, payload.flicker_command) < 65536 && pb_membersize(Command, payload.fade_command) < 65536 && pb_membersize(Command, payload.set_color_command) < 65536), YOU_MUST_DEFINE_PB_FIELD_32BIT_FOR_MESSAGES_Flicker_Fade_SetColor_Command)
#endif

#if !defined(PB_FIELD_16BIT) && !defined(PB_FIELD_32BIT)
/* If you get an error here, it means that you need to define PB_FIELD_16BIT
 * compile-time option. You can do that in pb.h or on compiler command line.
 * 
 * The reason you need to do this is that some of your messages contain tag
 * numbers or field sizes that are larger than what can fit in the default
 * 8 bit descriptors.
 */
PB_STATIC_ASSERT((pb_membersize(Command, payload.flicker_command) < 256 && pb_membersize(Command, payload.fade_command) < 256 && pb_membersize(Command, payload.set_color_command) < 256), YOU_MUST_DEFINE_PB_FIELD_16BIT_FOR_MESSAGES_Flicker_Fade_SetColor_Command)
#endif


/* @@protoc_insertion_point(eof) */
