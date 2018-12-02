import React from 'react'
import {
    BootstrapTable,
    TableHeaderColumn
} from 'react-bootstrap-table';

const Transactions = (props) => {
  
    return (
    <div>
        <BootstrapTable data={props.data} striped hover>
            <TableHeaderColumn isKey headerAlign='center' width='40%' dataField='sender'>
                Emisssor
        </TableHeaderColumn>
            <TableHeaderColumn dataField='recipient' headerAlign='center' width='40%'>
                Destinatário
        </TableHeaderColumn>
            <TableHeaderColumn dataField='amount' headerAlign='center' dataAlign='center'>
                Quantidade
        </TableHeaderColumn>
        </BootstrapTable>
    </div>
  )
}

export default Transactions;