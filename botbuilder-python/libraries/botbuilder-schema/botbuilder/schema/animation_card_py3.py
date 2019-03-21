# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AnimationCard(Model):
    """An animation card (Ex: gif or short video clip).

    :param title: Title of this card
    :type title: str
    :param subtitle: Subtitle of this card
    :type subtitle: str
    :param text: Text of this card
    :type text: str
    :param image: Thumbnail placeholder
    :type image: ~botframework.connector.models.ThumbnailUrl
    :param media: Media URLs for this card
    :type media: list[~botframework.connector.models.MediaUrl]
    :param buttons: Actions on this card
    :type buttons: list[~botframework.connector.models.CardAction]
    :param shareable: This content may be shared with others (default:true)
    :type shareable: bool
    :param autoloop: Should the client loop playback at end of content
     (default:true)
    :type autoloop: bool
    :param autostart: Should the client automatically start playback of media
     in this card (default:true)
    :type autostart: bool
    :param aspect: Aspect ratio of thumbnail/media placeholder, allowed values
     are "16:9" and "4:3"
    :type aspect: str
    :param value: Supplementary parameter for this card
    :type value: object
    """

    _attribute_map = {
        'title': {'key': 'title', 'type': 'str'},
        'subtitle': {'key': 'subtitle', 'type': 'str'},
        'text': {'key': 'text', 'type': 'str'},
        'image': {'key': 'image', 'type': 'ThumbnailUrl'},
        'media': {'key': 'media', 'type': '[MediaUrl]'},
        'buttons': {'key': 'buttons', 'type': '[CardAction]'},
        'shareable': {'key': 'shareable', 'type': 'bool'},
        'autoloop': {'key': 'autoloop', 'type': 'bool'},
        'autostart': {'key': 'autostart', 'type': 'bool'},
        'aspect': {'key': 'aspect', 'type': 'str'},
        'value': {'key': 'value', 'type': 'object'},
    }

    def __init__(self, *, title: str=None, subtitle: str=None, text: str=None, image=None, media=None, buttons=None, shareable: bool=None, autoloop: bool=None, autostart: bool=None, aspect: str=None, value=None, **kwargs) -> None:
        super(AnimationCard, self).__init__(**kwargs)
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.image = image
        self.media = media
        self.buttons = buttons
        self.shareable = shareable
        self.autoloop = autoloop
        self.autostart = autostart
        self.aspect = aspect
        self.value = value
