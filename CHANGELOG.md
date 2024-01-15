
[Unreleased]

Added

Changed

Fixed

[3.6.2] - 2024-01-15

Added
* Created CONTRIBUTING.md to help developers with making modifications to this repo

Changed

Fixed
* Typo for standard_high_multilingual model selection
* Code format

[3.6.1] - 2024-01-11

Added
* Added changelog to increase visibility of changes

Changed

Fixed
* Removed empty attributes from the request as some pydantic model changes will no longer accept them as valid request objects

[3.6.0] - 2023-12-22

Added
* Added proper dependencies for installing the client. 

Changed
* Updated the accuracys of EntityDetection to include high_automatic and standard_high_automatic. The default accuracy is now high_automatic

Fixed

[3.5.0] - 2023-11-14
NOTE: the versions of the client have been altered to match the version of Private AI's deidentification it should be used with. This change will only reflect the first 2 points of the release (in this case 3.5) while the third point will indicate changes to the client.

Added
* Added warning indicator if the version of the container doesn't match the version of the client

Changed

Fixed
* Fixed bug with reidentify_text where the incorrect object could be returned

[1.3.3] - 2023-11-14

Added
* Added reidentify_sensitive_labels attribute to the ReidentifyTextRequest object with the default set to True. If set to False, sensitive information (like credit card info) will not get reidentified in a reidentify request.
* Added best_labels to a processed text response object that returns an aggregation of all best_labels found in a process text operation.
* Added enable_non_max_suppression to the EntityDetection request object

Changed
*ProcessText objects will no longer contain entity_detection or processed_text by default. To maintain the previous behaviour, they can be added explicitly 
    (eg. req = process_text_obj(text=[], entity_detection=entity_detection_obj, processed_text=processed_text_obj))

Fixed
* bug fix with the reidentify_text function where passing in a dictionary instead of a request object would call the wrong function

[1.3.2] - 2023-09-11

Added
* Added new "max_resolution" PDF parameter, introduced in 3.3.3

Changed
* expanded the File request object list of file types to match what is supported in the deid service
* Changed audio start and end paddings to floats & default values to 0.5, the new default from releases 3.4 and on

Fixed

[1.3.1] 2023-08-08

Added

Changed
* Updated get_reidentify_entities to work with file responses.

Fixed

[1.3.0] - 2023-08-02


Added
* The client accepts url as an argument. the original initialization arguments (scheme, host, port) are still accepted. 
* Added get_diagnostic() to client to access the diagnostics endpoint 
* Response objects that include processed text have 2 new functions: get_reidentify_entities() which returns a list of Entity objects containing entities used and their original text, and get_reidentify_request which will return a reidentify request object, ready to use with the reidentify endpoint.

Changed
* requests made with the client that return a  Non-200 response now raise an HTTP Error.

Fixed
* Fixed issue where retreiving the properties of the response body (eg. processed_text) would not return a list if there was only one entry in the response
* Bug fix with block filter objects where entity_type couldn't be set

[1.2.0]

Added
* Added request objects and functions to for the reidentify endpoint

Changed


Fixed
* Bug fix for processed_text objects. Object can now be set to the appropriate type (MARKER, MASK or SYNTHETIC)

[1.1.0] - 2023-05-16

Added
* Added the capability to add authorization to the header of all requests for the client. 

Changed

Fixed
* Fixed a bug with the metrics endpoint

[1.0.5] - 2023-04-19

Added

Changed
* README updated with more detailed examples

Fixed

[1.0.4] - 2023-04-19

Added

Changed
* README updated with examples

Fixed

[1.0.3] - 2023-04-19

Added
* Initial client release

Changed

Fixed
