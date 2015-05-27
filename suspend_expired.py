from zdesk import Zendesk
import zendesk_util

from itertools import chain

from time import gmtime, strftime
import logging

def get_expired_organizations(organizations):
	'''Returns a list of organization ids for organizations with expired support contracts.

	Parameters
	----------
	organizations : list
		The list of organizations to extract organization ids from.

	Returns
	-------
	list of ints
		A list of organization ids of organizations with expired support contracts.
	'''
	return [organization for organization in organizations 
		if (organization['organization_fields']['support_level'] == "expired_support")]


def ensure_suspended_users(zendesk, organization):
	'''Suspends all users in an organization.

	Parameters
	----------
	zendesk : Zendesk object
		The Zendesk object being used to interact with the Zendesk REST API.

	organization : int
		The id of the organization for which we will suspend all users.
	'''
	users = zendesk_util.get_users(zendesk, organization['id'])
	for user in users:
		if not user['suspended']:
			logging.info(organization['name'] + " : " + user['name'])
			zendesk.user_update(id=user['id'], data={"user": {"suspended": True}})

# --------------- #
# Main code block #
# --------------- #

logging.basicConfig(filename='suspend_expired_' + strftime("%Y-%m-%d_%H.%M.%S", gmtime()) + '.log', level=logging.INFO)

zendesk = Zendesk('https://<organization>.zendesk.com', '<email_address>', '<password>')
organizations = zendesk_util.get_organizations(zendesk)
expired_organizations = get_expired_organizations(organizations)

for expired_organization in expired_organizations:
	ensure_suspended_users(zendesk, expired_organization)