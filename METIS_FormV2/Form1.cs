using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO.Ports;

namespace METIS_FormV2
{
    public partial class Form1 : Form
    {
        #region Variables
        int serialDataIn;
        int index = 0;
        int[] dataArray = new int[50];

        #endregion

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            btnOpenPort.Enabled = true;
            btnClosePort.Enabled = false;
            cbBaudRate.Text = "9600";
            txbADC.Enabled = false;

            chartData.Series["Data"].Points.AddXY(1, 1);
        }

        #region Buttons
        private void btnOpenPort_Click(object sender, EventArgs e)
        {
            try
            {
                serialPort1.PortName = cbComPorts.Text;
                serialPort1.BaudRate = Convert.ToInt32(cbBaudRate.Text);
                serialPort1.Open();

                btnOpenPort.Enabled = false;
                btnClosePort.Enabled = true;
                cbComPorts.Enabled = false;
                cbBaudRate.Enabled = false;

                chartData.Series["Data"].Points.Clear();
            }
            catch(Exception error)
            {
                MessageBox.Show(error.Message);
            }
        }

        private void btnClosePort_Click(object sender, EventArgs e)
        {
            try
            {
                serialPort1.Close();

                btnOpenPort.Enabled = true;
                btnClosePort.Enabled = false;
                cbComPorts.Enabled = true;
                cbBaudRate.Enabled = true;
            }
            catch (Exception error)
            {
                MessageBox.Show(error.Message);
            }
        }
        #endregion

        #region ComboBox
        private void cbComPorts_DropDown(object sender, EventArgs e)
        {
            string[] portsList = SerialPort.GetPortNames();
            cbComPorts.Items.Clear();
            cbComPorts.Items.AddRange(portsList);
        }




        #endregion

        #region Data Reception
        private void serialPort1_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            serialDataIn = serialPort1.ReadByte();
            this.BeginInvoke(new EventHandler(UpdateArray));
        }

        private void UpdateArray(object sender, EventArgs e)
        {
            try
            {
                if (index < dataArray.Length - 1)
                {
                    chartData.Series["Data"].Points.AddY(serialDataIn);
                    index++;
                }
                else
                {
                    ShiftData(dataArray, serialDataIn);
                    chartData.Series["Data"].Points.Clear();
                    for (int i = 0; i < dataArray.Length - 1; i++)
                    {
                        chartData.Series["Data"].Points.AddY(dataArray[i]);
                    }
                }
            }
            catch (Exception error)
            {
                MessageBox.Show(error.Message);
            }
        }

        private void ShiftData(int[] array, int newValue)
        {
            for (int i = 1; i < array.Length; i++)
            {
                array[i - 1] = array[i];
                array[array.Length - 1] = newValue;
            }
        }

        #endregion
    }
}
