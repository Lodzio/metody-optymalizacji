import React from "react";
import { Input, Button } from "@material-ui/core";
import axios from "axios";

class App extends React.Component {
  state = {
    params: {
      function: "(x1-2)^2+(x2-1)^2",
      g1: "x1^2-x2",
      g2: "x1+x2-2",
      g3: "",
      x1: "-10",
      x2: "-6",
    },
    result: {
      pos: [],
      logs: [],
      g: [],
    },
    error: "",
  };
  onGenerate = () => {
    axios
      .get("http://127.0.0.1:5000/", { params: this.state.params })
      .then((result) => {
        console.log(result.data);
        this.setState({ result: result.data, error: "" });
      })
      .catch((error) => {
        console.error(error);
        this.setState({ error: "nie udało się wygenerować" });
      });
  };
  onChange = (event) => {
    const params = { ...this.state.params };
    params[event.target.id] = event.target.value;
    this.setState({ params });
  };
  withLabel(label, Input) {
    return (
      <div style={{ display: "flex", flexDirection: "row", alignItems: "end" }}>
        <div style={{ width: "120px" }}>{label}</div>
        {Input}
      </div>
    );
  }
  render() {
    return (
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div style={{ maxWidth: "30%" }}>
          {this.withLabel("function", <Input id="function" onChange={this.onChange} />)}
          {this.withLabel("g1", <Input id="g1" onChange={this.onChange} />)}
          {this.withLabel("g2", <Input id="g2" onChange={this.onChange} />)}
          {this.withLabel("g3", <Input id="g3" onChange={this.onChange} />)}
          {this.withLabel("x1", <Input id="x1" onChange={this.onChange} />)}
          {this.withLabel("x2", <Input id="x2" onChange={this.onChange} />)}
          {this.withLabel("localStepSize", <Input id="localStepSize" onChange={this.onChange} />)}
          {this.withLabel("epsilon", <Input id="epsilon" onChange={this.onChange} />)}
          {this.withLabel("stepsLimit", <Input id="stepsLimit" onChange={this.onChange} />)}
          <Button onClick={this.onGenerate}>Generate</Button>
        </div>
        <div style={{ marginTop: "20px" }}>result: [{String(this.state.result.pos)}]</div>
        {this.state.result.logs.map((log) => (
          <div key={log} style={{ marginTop: "20px" }}>
            {String(log)}
          </div>
        ))}
        {this.state.result.g.map((g, i) => (
          <div key={i} style={{ marginTop: "20px" }}>
            g{i}:{String(g)}
          </div>
        ))}{" "}
        {this.state.error && <div>{this.state.error}</div>}
      </div>
    );
  }
}

export default App;
