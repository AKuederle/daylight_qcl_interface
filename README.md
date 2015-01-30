## daylight_qcl_interface

Daylight_qcl_interface is a python based wrapper for several serial interface commands to control a Daylight Solution Tunable laser controller.

It Provides:
1. A simple wrapper class for a a selection of serial port commands to control a daylight solution tunable QCL.
2. More advanced functions to provide some higher level functionality

The documentation of the Controllers serial interface can be found in its manual (Available with the product).

### Usage
The qcl_controller.py includes a QCL class. It can be used in an interactive Python shell or in a arbitrary python script by importing the module and creating an instance of the class.
The provided functions (see class docstring) can than be used to control the laser.

#### Example

```python
import qcl_controller # makes the QCL() class available in the current python session or script (make sure qcl_controller.py is in the working directory or the path)
qcl = QCL() # establish the connection to the QCL

# Set and get using the direct function calls
print qcl.get_wn() # gets the current wavenumber and prints it out
qcl.set_wn(1080) # sets the wavenumber to 1080 cm-1

# Set and get using the namedtuple container
print qcl.Get.wn() # gets the current wavenumber and prints it out
qcl.Set.wn(1080) # sets the wavenumber to 1080 cm-1
```
"""

### License
daylight_qcl_interface is published under the MIT license.
