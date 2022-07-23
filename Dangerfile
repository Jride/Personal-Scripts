can_merge = github.pr_json["mergeable"]
warn("This PR cannot be merged yet.") unless can_merge

contains_version_file = (git.added_files + git.modified_files).any? { |path| path.include?(".version") }

if !contains_version_file
    
    message = "Oops! It looks like you forgot to bump the version number of the scripts.\n\n"
    
    message << "You can bump the version of the scripts by updating the `.version` file in the root of the repository. Please follow the the [Semantic Versioning](https://semver.org/) strategy."

    fail(message)
end