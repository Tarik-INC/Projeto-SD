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
                Remetente
        </TableHeaderColumn>
            <TableHeaderColumn dataField='recipient' headerAlign='center' width='40%'>
                Emissor
        </TableHeaderColumn>
            <TableHeaderColumn dataField='amount' headerAlign='center'>
                Quantidade
        </TableHeaderColumn>
        </BootstrapTable>
    </div>
  )
}

export default Transactions;