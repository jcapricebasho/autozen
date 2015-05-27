def get_organizations(zendesk):
	'''Returns a list of Organizations from Zendesk.

	Returns
	-------
	list
		List of organizations in Zendesk.
	'''
	page = 0
	cont = True
	organizations = []

	while cont:
		page += 1
		response = zendesk.organizations_list(page=page)
		organizations.extend(response['organizations'])
		cont = response['next_page'] != None

	return organizations

def get_users(zendesk, id):
	'''Returns a list of Users for the given organization id.

	Parameters
	----------
	id : int
		The Zendesk id of the organization to retrieve users from.

	Returns
	-------
	list
		List of users for specified organization.
	'''
	page = 0
	cont = True
	users = []

	while cont:
		page +=1
		response = zendesk.organization_users(id=id, page=page)
		users.extend(response['users'])
		cont = response['next_page'] != None

	return users