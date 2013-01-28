/*
@author Rik Vermeer
@repo http://github.com/rikvermeer/pispiled/modules/lpd8806

@license I believe GPL2

c python extension module that writes bytes to the lpd8806 chip on the raspberry-pi

set(bits_per_word, speed_hz, delay)
write(([0, 128, 255]))

*/

#include <Python.h>
#include <stdio.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

#define ARRAY_SIZE(a) (sizeof(a) / sizeof((a)[0]))
 
static const char *device = "/dev/spidev0.0";
static uint8_t bits = 8;
static uint32_t speed = 20000000;
static uint16_t delay = 0;
static int fd;
static uint8_t lpd8806_gamma[256] = {
       128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128,
       128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128,
       128, 128, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129,
       129, 129, 129, 129, 129, 130, 130, 130, 130, 130, 130, 130, 130,
       130, 131, 131, 131, 131, 131, 131, 131, 131, 132, 132, 132, 132,
       132, 132, 132, 133, 133, 133, 133, 133, 134, 134, 134, 134, 134,
       135, 135, 135, 135, 135, 136, 136, 136, 136, 137, 137, 137, 137,
       138, 138, 138, 138, 139, 139, 139, 140, 140, 140, 141, 141, 141,
       141, 142, 142, 142, 143, 143, 144, 144, 144, 145, 145, 145, 146,
       146, 146, 147, 147, 148, 148, 149, 149, 149, 150, 150, 151, 151,
       152, 152, 152, 153, 153, 154, 154, 155, 155, 156, 156, 157, 157,
       158, 158, 159, 160, 160, 161, 161, 162, 162, 163, 163, 164, 165,
       165, 166, 166, 167, 168, 168, 169, 169, 170, 171, 171, 172, 173,
       173, 174, 175, 175, 176, 177, 178, 178, 179, 180, 180, 181, 182,
       183, 183, 184, 185, 186, 186, 187, 188, 189, 190, 190, 191, 192,
       193, 194, 195, 195, 196, 197, 198, 199, 200, 201, 202, 202, 203,
       204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216,
       217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229,
       230, 232, 233, 234, 235, 236, 237, 238, 239, 241, 242, 243, 244,
       245, 246, 248, 249, 250, 251, 253, 254, 255};


static PyObject *
LPD8806_set(PyObject *self, PyObject *args)
{
	if(!PyArg_ParseTuple(args, "bIH", &bits, &speed, &delay))
		return NULL;
	return Py_BuildValue("bIH", bits, speed, delay);
}

static PyObject *
LPD8806_write(PyObject *self, PyObject *args)
{
	PyObject* obj;
    PyObject* seq;
    int i, len;
    if (!PyArg_ParseTuple(args, "O", &obj))
        return NULL;

    seq = PySequence_Fast(obj, "expected a sequence");
    Py_INCREF(seq);
    len = PySequence_Size(obj);
	uint8_t items[len+1];
    for (i = 0; i < len; i++) {
		PyObject *item = PySequence_Fast_GET_ITEM(seq, i);
		int x = PyInt_AsLong(item);
		items[i] = lpd8806_gamma[x];
    }
    items[len] = 0;
    Py_DECREF(seq);
	struct spi_ioc_transfer tr = {
		.tx_buf = (unsigned long)items,
 		.len = ARRAY_SIZE(items),
 		.delay_usecs = delay,
		.speed_hz = speed,
		.bits_per_word = bits,
	};
	int ret = ioctl(fd, SPI_IOC_MESSAGE(1), &tr);
	return Py_BuildValue("i", ret);
}

static PyMethodDef lpd8806_methods[] = {
	{"write", LPD8806_write, METH_VARARGS, "Write bites (Raspberry pi-REV2 -> SPI -> LPD8806"},
	{"set", LPD8806_set, METH_VARARGS, "Sets the bits/word, speed and delay"},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initlpd8806()
{
	(void)Py_InitModule("lpd8806", lpd8806_methods);
	fd = open(device, O_RDWR);
}
