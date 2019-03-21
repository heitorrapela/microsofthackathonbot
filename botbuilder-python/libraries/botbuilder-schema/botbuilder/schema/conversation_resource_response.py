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


class ConversationResourceResponse(Model):
    """A response containing a resource.

    :param activity_id: ID of the Activity (if sent)
    :type activity_id: str
    :param service_url: Service endpoint where operations concerning the
     conversation may be performed
    :type service_url: str
    :param id: Id of the resource
    :type id: str
    """

    _attribute_map = {
        'activity_id': {'key': 'activityId', 'type': 'str'},
        'service_url': {'key': 'serviceUrl', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ConversationResourceResponse, self).__init__(**kwargs)
        self.activity_id = kwargs.get('activity_id', None)
        self.service_url = kwargs.get('service_url', None)
        self.id = kwargs.get('id', None)
