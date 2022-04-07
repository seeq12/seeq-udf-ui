# User Guide

A general overview of the motivation for and functionality of the Seeq UDF Editor, as implemented in
**seeq-udf-ui** is provided in this section.

## Motivation

The Seeq Formula Tool is part of Seeq core product that allows the user to use a rich library of
formulas including mathematical, statistics, and special purpose thermodynamic and fluid mechanic
relationships. The Formula Tool also allows the user to customize the formula to their application
but it doesn't allow them to save the custom formula. To do so, user-defined formula functions (UDFs)
are provided in Seeq. UDFs are not bound to any signal and allow the users to create their own
custom formula function, save them for future use and apply them to various assets. The current
limitation is that creating UDFs requires familiarity with the Seeq API and/or Python sdk. 
UDFs are objects with various attributes such as examples, description, access control, etc. and to 
create a UDF, these properties have to be set through the appropriate API calls. The UDF Editor tool
provides a UI and creates the API calls in the backend so that creating and modifying UDFs is easier
for the user. 

## Usage


<details open="" class="details-reset border rounded-2">
  <summary class="px-3 py-2 border-bottom">
    <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-device-camera-video">
    <path fill-rule="evenodd" d="M16 3.75a.75.75 0 00-1.136-.643L11 5.425V4.75A1.75 1.75 0 009.25 3h-7.5A1.75 1.75 0 000 4.75v6.5C0 12.216.784 13 1.75 13h7.5A1.75 1.75 0 0011 11.25v-.675l3.864 2.318A.75.75 0 0016 12.25v-8.5zm-5 5.075l3.5 2.1v-5.85l-3.5 2.1v1.65zM9.5 6.75v-2a.25.25 0 00-.25-.25h-7.5a.25.25 0 00-.25.25v6.5c0 .138.112.25.25.25h7.5a.25.25 0 00.25-.25v-4.5z"></path>
    </svg>
    <span aria-label="Video description _static/user_manual.mp4" class="m-1">User Define Function Add-on Usage</span>
    <span class="dropdown-caret"></span>
  </summary>

<video src="_static/user_manual.mp4"
poster="_static/overview.png"
controls="controls" muted="muted" class="d-block rounded-bottom-2 width-fit" style="max-width:700px;
background:transparent url('_static/overview.png') no-repeat 0 0;
-webkit-background-size:cover; -moz-background-size:cover; -o-background-size:cover; background-size:cover;"
webboost_found_paused="true" webboost_processed="true">
</video>
</details>

### Step 1 - UDF Search or Create
- Under packages, you will see all packages that you have at least read access to. You may select one from the existing packages
on the server or type a new package name
<table>
   <td>
      <img alt="image" src="_static/package.png" width="500" height="200">
   </td>
</table>

- Under functions, you will see the functions under the selected package (if any). You may also enter a new function name
to create a new function.
- Different variations of functions can be created with the same name and different input arguments. This is
reflected in the way the functions are displayed. For instance `function1($signal, $signal)` and
`function1($signal, $scalar)` are different objects.
- If creating a new function, you should not include the input arguments or the brackets (for example type `newfunction`)

<table>
   <td>
      <img alt="image" src="_static/function.png" width="500" height="200">
   </td>
</table>


### Step 2 - Inputs and Formula

- Add new parameters, delete a parameter from the list, and select the parameter type (signal, scalar, condition)
- You can insert the parameters created in the formula editor box using the '+' button next to the parameter.
- Type the formula in the formula editor box. The formula should follow the Seeq formula syntax. 

<table>
   <td>
      <img alt="image" src="_static/formula.png" width="500" height="200">
   </td>
</table>

- You may also type in or paste the formula in the editor first, and then use the formula parser button
to parse the parameters and list them. While this method can save you some time in typing long formulas,
it is error-prone, and you should verify the validity of the extracted parameters. The type of parsed
parameters is set to scalar as default and should be changed manually if needed.

### Step 3 - UDF Documentation
- You may enter a description of the package and the formula function in the provided boxes. 
The markdown box supports markdown
language for description and automatically updates the html box. You may also select the html
tab from the bottom of the description box and directly edit the html box,
which will in turn update the markdown box. You may also view the final processed html by clicking 
on the respective tab.

<table>
   <td>
      <img alt="image" src="_static/description.png" width="500" height="200">
   </td>
</table>

- You may add examples and descriptions of the examples (optional)

<table>
   <td>
      <img alt="image" src="_static/examples.png" width="500" height="200">
   </td>
</table>

### Step 4 - Access Control
- You may search for Seeq users and usergroups in the provided search box, and grant them
read, right, or manage access. By default, the table is filled with the current user given all access, 
however, you may modify or even remove your access from the list (you will lose access to the formula you created).
- Access applies to the packages, not functions, and admin users always have access to packages
regardless of the access management set for the package.

<table>
   <td>
      <img alt="image" src="_static/access.png" width="500" height="200">
   </td>
</table>

### Step 4 - Review and Submit
- Upon clicking on Review, a confirmation box will appear where you can view the details of what you 
are about to submit (push) to Seeq

<table>
   <td>
      <img alt="image" src="_static/review.png" width="500" height="200">
   </td>
</table>

- You may also delete a package or function. After clicking on Delete, a pop-up will appear
asking you to choose whether you would like to delete the function or package.
- Deleting a UDF would "archive" it and not permanently delete it. However, it will no longer appear in the search
- You may create a package with the same name as an existing but archived package, which will unarchive
the package. But doing so with a function results in an error (modifying this behavior is outside the
scope of this tool).

<table>
   <td>
      <img alt="image" src="_static/delete.png" width="500" height="200">
   </td>
</table>


