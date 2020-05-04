import React, { Component } from 'react';
import UsersService from '../services/UsersService';

const usersService = new UsersService();

class UserCreateUpdate extends Component {
    constructor(props) {
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this);
      }

      componentDidMount(){
        const { match: { params } } = this.props;
        if(params && params.pk)
        {
          usersService.getUser(params.pk).then((u)=>{
            this.refs.name.value = u.name;
            this.refs.cpf.value = u.cpf;
            this.refs.email.value = u.email;
            this.refs.phone.value = u.phone;
            this.refs.address.value = u.address;
          })
        }
      }

      handleCreate(){
        usersService.createUser(
          {
            "name": this.refs.firstName.value,
            "cpf": this.refs.cpf.value,
            "email": this.refs.email.value,
            "phone": this.refs.phone.value,
            "address": this.refs.address.value
        }
        ).then((result)=>{
          alert("User created!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      }
      handleUpdate(pk){
        usersService.updateUser(
          {
            "pk": pk,
            "name": this.refs.name.value,
            "cpf": this.refs.cpf.value,
            "email": this.refs.email.value,
            "phone": this.refs.phone.value,
            "address": this.refs.address.value
        }
        ).then((result)=>{
          console.log(result);
          alert("User updated!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      }
      handleSubmit(event) {console.log("OLLLAAAAR");
        const { match: { params } } = this.props;

        if(params && params.pk){
          this.handleUpdate(params.pk);
        }
        else
        {
          this.handleCreate();
        }

        event.preventDefault();
      }

      render() {
        return (
          <form onSubmit={this.handleSubmit}>
          <div className="form-group">
            <label>
              Name:</label>
              <input className="form-control" type="text" ref='name' />

            <label>
              Cpf:</label>
              <input className="form-control" type="text" ref='cpf'/>

            <label>
              Phone:</label>
              <input className="form-control" type="text" ref='phone' />

            <label>
              Email:</label>
              <input className="form-control" type="text" ref='email' />

            <label>
              Address:</label>
              <input className="form-control" type="text" ref='address' />

            <input className="btn btn-primary" type="submit" value="Submit" />
            </div>
          </form>
        );
      }
}

export default UserCreateUpdate;