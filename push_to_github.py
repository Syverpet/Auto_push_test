from github import Github

# First create a Github instance:

# using an access token
g = Github("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")

# Github Enterprise with custom hostname
#g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

# Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)


# access files in repo
repo_OI = g.get_user().get_repo("prototyping_data_april_2022")
contents = repo_OI.get_contents("test.txt")
print(contents)




# Update files in repo


contents = repo_OI.get_contents("test.txt")

print(contents.path)

repo.update_file('syverpet', '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', contents.path, "more tests", "more tests", contents.sha)


# Update files in repo
#sha = repo.get_contents('test').sha
#repo.update_file(
#	path = 'test', 
#	message = 'Update test using GithubAPI', 
#	content = base64.b64encode('updated test'), 
#	committer=InputGitAuthor("vinayakvivek", email, "2016-01-15T16:13:30+12:00"),
#	author=InputGitAuthor("vinayakvivek", email, "2016-01-15T16:13:30+12:00"),
#	sha = sha, branch = 'master')