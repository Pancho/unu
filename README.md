# djangoutils

* need to restructure the imports as there are problems with usage

* add skeleton.html if none is present yet
* fix views imports after adding new view
* make an option for which apps we want to fix JS namespaces (not all need one)

* need the common management commands
  
* SPROO
    * installer (which means that most of the following will live in SPROO repo)
    * generator UI
        * components should be bundles in their own folders, as should pages. think more on the structure of a sample project
        * should this one also generate django endpoints?
    * state manager (as simple as they come, event based)
        subscribing and unsubscribing must be automatic and I don't care if it's via convention of whatever, but it must not be a route for memory leaks