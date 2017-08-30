/* MTD functions for Python, based on:
 *  http://www.opensourceforu.com/2012/01/working-with-mtd-devices/
 * Copyright (C) 2017 Topic Embedded Products
 */
#include <Python.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <mtd/mtd-user.h>


static PyObject* erase_sector(PyObject *self, PyObject *args)
{
    int fd;
	erase_info_t ei;
    int ret;

    if (!PyArg_ParseTuple(args, "iii", &fd, &ei.start, &ei.length))
        return NULL;
    
    /* Most MTD drivers don't really implement unlock, and code never
     * checks the result from this because it's usually EOPNOTSUPP */
    ioctl(fd, MEMUNLOCK, &ei);
    ret = ioctl(fd, MEMERASE, &ei);
    if (ret < 0)
		return PyErr_SetFromErrno(PyExc_IOError);
	
	return Py_BuildValue("i", ret);
}


static int mtd_get_info(int fd, mtd_info_t* info)
{
	return ioctl(fd, MEMGETINFO, info);
}

static PyObject* get_info(PyObject *self, PyObject *args)
{
    int fd;
    mtd_info_t mtd_info;

    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;
    
    if (mtd_get_info(fd, &mtd_info) < 0)
		return PyErr_SetFromErrno(PyExc_IOError);
    
    return Py_BuildValue("iii", mtd_info.type, mtd_info.size, mtd_info.erasesize);
}

static PyMethodDef mtd_methods[] = {
    {"get_info", get_info, METH_VARARGS,
		"Get MTD info, call with FD, returns (type,size,erasesize)."},
    {"erase_sector", erase_sector, METH_VARARGS,
		"Erase flash sector. Call with (fd,start,sectorsize)."},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initmtd(void)
{
    (void) Py_InitModule("mtd", mtd_methods);
}
